import json
import time
import redis
import uuid
from datetime import datetime
from logs.log_config import get_custom_logger


class TokenManager:
    """
    Клас для управління токеном.
    """

    @staticmethod
    def generate_token():
        """
        Генерує і зберігає унікальний токен з використанням UUID4.

        :return: Унікальний токен у форматі рядка.
        """
        return str(uuid.uuid4())


class MyRedis:
    """
    Клас для роботи з Redis.
    """

    def __init__(self, host: str, port: int, database: int):
        """
        Ініціалізація класу MyRedis.

        :param host: Адреса сервера Redis.
        :param port: Порт сервера Redis.
        :param database: Номер бази даних Redis.
        """
        self.host = host
        self.port = port
        self.database_name = database
        self.client = None
        self.logger = get_custom_logger("message_redis.json")
        self.session_key = None

    def __enter__(self):
        """
        Встановлює підключення до Redis при вході в контекстний менеджер.

        :return: Екземпляр класу MyRedis.
        :raises redis.ConnectionError: Якщо не вдається підключитися до Redis.
        """
        try:
            self.client = redis.Redis(host=self.host, port=self.port, db=self.database_name)
            self.client.ping()
            self.logger.info(['redis', 'connected'], db_name=self.database_name)
            return self
        except redis.ConnectionError as e:
            self.logger.error(['redis', 'connection_error'], error=str(e))
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закриває підключення до Redis при виході з контекстного менеджера.

        :param exc_type: Тип виключення.
        :param exc_value: Значення виключення.
        :param traceback: Слід виключення.
        """
        if self.client:
            self.client.close()
            self.logger.info(['redis', 'disconnected'])
        if exc_type:
            self.logger.error(['general', 'exception_in_with_block'], error=str(exc_value))
        return False

    def init_user_id(self, user_id):
        """
        Ініціалізація ключа для сесії користувача.

        :param user_id: Ідентифікатор користувача.
        """
        # Создание уникального ключа сессии для каждого пользователя
        self.session_key = f"user_session:{user_id}"

    @staticmethod
    def convert_login_time(session_info_decoded):
        """
        Конвертує час логіна з UNIX у читабельний формат.

        :param session_info_decoded: Розкодована інформація про сесію.
        :return: Час логіна у форматі 'YYYY-MM-DD HH:MM:SS' або None, якщо не знайдено.
        """
        if 'login_time' in session_info_decoded:
            session_inf = int(session_info_decoded['login_time'])
            format_time = '%Y-%m-%d %H:%M:%S'
            login_time = datetime.fromtimestamp(session_inf).strftime(format_time)
            return login_time
        return None

    def session_exists(self, user_id):
        """
        Перевірка наявності сесії користувача.

        :param user_id: Ідентифікатор користувача.
        :return: True, якщо сесія існує, інакше False.
        """
        self.init_user_id(user_id)
        return self.client.exists(self.session_key)

    def create_session_user(self, user_id):
        """
        Створює сесію користувача в Redis, якщо вона не існує.

        :param user_id: Ідентифікатор користувача.
        """
        self.init_user_id(user_id)
        if not self.session_exists(user_id):
            login_time = int(time.time())
            # Генерация нового токена для каждого пользователя
            session_token = TokenManager.generate_token()

            session_data = {
                "session_token": session_token,
                "login_time": login_time
            }

            # Зберігання сесії по user_id
            self.client.hset(self.session_key, mapping=session_data)

            # Зберігання user_id по session_token
            self.client.set(f"session_token:{session_token}", user_id)

            self.client.expire(self.session_key, 1800)

            # Логування факту збереження даних
            saved_user_id = self.client.get(f"session_token:{session_token}")
            if saved_user_id:
                self.logger.info(
                    ["general", "session_token_saved"],
                    session_token=session_token,
                    user_id=saved_user_id.decode('utf-8')
                )
            else:
                self.logger.error(["general", "session_token_not_saved"], session_token=session_token)

            readable_login_time = self.convert_login_time(self.get_session())

            self.logger.info(
                ["general", "save_session"],
                session_token=session_token,
                login_time=readable_login_time
            )
        else:
            self.logger.info(["general", "session_exists"], user_id=user_id)

    def get_session(self):
        """
        Отримати активну сесію для поточного користувача.

        :return: Інформація про сесію.
        """
        session_inf = self.universal_decoder(self.session_key)
        return session_inf

    def get_user_id_by_token(self, session_token):
        """
        Отримати user_id по session_token.

        :param session_token: Токен сесії.
        :return: Ідентифікатор користувача або None, якщо не знайдено.
        """
        user_id = self.client.get(f"session_token:{session_token}")
        if user_id:
            return user_id.decode('utf-8')
        else:
            self.logger.error(["general", "user_id_not_found_by_token"], session_token=session_token)
            return None

    def universal_decoder(self, key):
        """
        Універсальний декодер для всіх типів даних з Redis.

        :param key: Ключ для декодування.
        :return: Розкодовані дані у вигляді рядка, списку або словника.
        """
        key_type = self.client.type(key).decode('utf-8')

        if key_type == 'string':
            return self.client.get(key).decode('utf-8')

        elif key_type == 'hash':
            return {k.decode('utf-8'): v.decode('utf-8') for k, v in self.client.hgetall(key).items()}

        elif key_type == 'list':
            return [item.decode('utf-8') for item in self.client.lrange(key, 0, -1)]

        elif key_type == 'set':
            return [item.decode('utf-8') for item in self.client.smembers(key)]

        elif key_type == 'zset':
            return [item.decode('utf-8') for item in self.client.zrange(key, 0, -1)]

        else:
            return f"Unsupported key type: {key_type}"

    def database_to_json(self):
        """
        Експортує всі дані з Redis у JSON.
        """
        keys = self.client.keys()
        data = {}

        for key in keys:
            key_str = key.decode('utf-8')
            data[key_str] = self.universal_decoder(key_str)

        with open('redis_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.logger.info(["general", "export_data"])

    def update_last_activity(self, user_id):
        """
        Оновлює час останньої активності користувача.

        :param user_id: Ідентифікатор користувача.
        """
        self.init_user_id(user_id)

        if self.session_key is None:
            self.logger.error(['general', 'session_key_error'])
            return

        current_time = int(time.time())

        # Оновлюємо поле login_time в хеш-таблиці користувача
        self.client.hset(self.session_key, "login_time", current_time)

        # Оновлюємо TTL для продовження часу життя сесії
        self.client.expire(self.session_key, 1800)

        # Логування успішної операції
        self.logger.info(["general", "update_last_activity"])

        self.updated_session_info()

    def delete_session(self, user_id):
        """
        Видалення сесії для користувача та відповідного session_token.

        :param user_id: Ідентифікатор користувача.
        """
        self.init_user_id(user_id)

        # Отримуємо інформацію про сесію
        session_info = self.get_session()

        if session_info:
            session_token = session_info.get('session_token')

            # Видаляємо саму сесію
            self.client.delete(self.session_key)
            self.logger.info(["general", "delete_session"], user_id=user_id)

            # Видаляємо інформацію про session_token
            if session_token:
                self.client.delete(f"session_token:{session_token}")
                self.logger.info(["general", "delete_session_token"], session_token=session_token)
            else:
                self.logger.error(["general", "token_not_found_in_session"], user_id=user_id)
        else:
            self.logger.error(["general", "session_not_found"], user_id=user_id)

    def updated_session_info(self):
        """
        Логування оновленої інформації про сесію користувача.
        """
        updated_session_info = self.get_session()
        if updated_session_info:
            session_token = updated_session_info.get('session_token')
            login_time = self.convert_login_time(updated_session_info)
            user_id = self.get_user_id_by_token(session_token)

            if user_id:
                self.logger.info(
                    ["general", "updated_session_info"],
                    user_id=user_id,
                    session_token=session_token,
                    login_time=login_time
                )
            else:
                self.logger.error(["general", "user_id_not_found"], session_token=session_token)
        else:
            self.logger.error(["general", "session_not_found"])

    def delete_all_data(self):
        """
        Видаляє всі дані в усіх базах даних Redis.
        """
        self.client.flushall()
        self.logger.info(["redis", "delete_all_data"])


if __name__ == "__main__":
    with MyRedis("192.168.20.181", 6379, 0) as redis_instance:
        # Створюємо сесію, якщо вона не існує
        redis_instance.create_session_user("ayu")
        redis_instance.create_session_user("viki")

        # Оновлюємо час останньої активності
        redis_instance.update_last_activity("ayu")
        redis_instance.update_last_activity("viki")

        # Видаляємо сесію
        redis_instance.delete_session("ayu")
        redis_instance.delete_session("viki")


        # redis_instance.delete_all_data()

        # Експорт даних у JSON
        redis_instance.database_to_json()
