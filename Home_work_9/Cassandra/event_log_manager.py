import json
import uuid
from gevent import monkey
monkey.patch_all()
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timedelta
from logs.log_config import get_custom_logger


class EventLogManager:
    """
    Клас для управління логами подій у Cassandra.
    """

    def __init__(self, host: str, port: int, keyspace: str, username: str, password: str):
        """
        Ініціалізація класу для підключення до Cassandra.

        :param host: Хост сервера Cassandra.
        :param port: Порт сервера Cassandra.
        :param keyspace: Ім'я ключового простору (keyspace).
        :param username: Ім'я користувача для аутентифікації.
        :param password: Пароль для аутентифікації.
        """
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.username = username
        self.password = password
        self.session = None
        self.logger = get_custom_logger("message_cassandra.json")

    def __enter__(self):
        """
        Підключення до Cassandra при вході в контекстний менеджер.

        :return: Екземпляр класу EventLogManager.
        :raises ConnectionError: Якщо не вдається підключитися до Cassandra.
        """
        try:
            auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)
            cluster = Cluster([self.host], port=self.port, auth_provider=auth_provider)
            self.session = cluster.connect(self.keyspace)
            self.logger.info(['cassandra', 'connected'], keyspace=self.keyspace)
            return self
        except Exception as e:
            self.logger.error(['cassandra', 'connection_error'], error=str(e))
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закриття підключення до Cassandra при виході з контекстного менеджера.

        :param exc_type: Тип виключення.
        :param exc_value: Значення виключення.
        :param traceback: Слід виключення.
        """
        if self.session:
            self.session.shutdown()
            self.logger.info(['cassandra', 'disconnected'])
        if exc_type:
            self.logger.error(['general', 'exception_in_with_block'], error=str(exc_value))
        return False

    def create_event_log_table(self):
        """
        Створення таблиці для зберігання логів подій.
        """
        query = """
        CREATE TABLE IF NOT EXISTS event_logs (
            event_id UUID PRIMARY KEY,
            user_id UUID,
            event_type TEXT,
            timestamp TIMESTAMP,
            metadata TEXT
        );
        """
        self.session.execute(query)
        self.logger.info(['cassandra', 'table_created'], table_name='event_logs')

    def create_event_log(self, user_id: uuid.UUID, event_type: str, metadata: str):
        """
        Додавання нового лога події.

        :param user_id: Ідентифікатор користувача.
        :param event_type: Тип події.
        :param metadata: Додаткова інформація про подію.
        """
        event_id = uuid.uuid4()
        timestamp = datetime.now()
        query = """
        INSERT INTO event_logs (event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.session.execute(query, (event_id, user_id, event_type, timestamp, metadata))
        self.logger.info(['cassandra', 'event_created'], event_id=event_id, user_id=user_id)

    def read_events_by_type(self, event_type: str):
        """
        Отримання всіх подій певного типу за останні 24 години.

        :param event_type: Тип події для пошуку.
        :return: Список подій.
        """
        last_24_hours = datetime.now() - timedelta(hours=24)
        query = """
        SELECT * FROM event_logs
        WHERE event_type=%s AND timestamp >= %s ALLOW FILTERING
        """
        rows = self.session.execute(query, (event_type, last_24_hours))
        return rows.all()

    def update_event_metadata(self, event_id: uuid.UUID, new_metadata: str):
        """
        Оновлення поля metadata для події.

        :param event_id: Ідентифікатор події.
        :param new_metadata: Нова інформація для поля metadata.
        """
        query = """
        UPDATE event_logs SET metadata = %s WHERE event_id = %s
        """
        self.session.execute(query, (new_metadata, event_id))
        self.logger.info(['cassandra', 'event_updated'], event_id=event_id)

    def delete_old_events(self):
        """
        Видалення подій старших за 7 днів.
        """
        older_than_7_days = datetime.now() - timedelta(days=7)

        # Сначала получаем все события старше 7 дней
        select_query = """
        SELECT event_id FROM event_logs WHERE timestamp < %s ALLOW FILTERING
        """
        rows = self.session.execute(select_query, (older_than_7_days,))

        # Удаляем каждое событие по event_id
        delete_query = """
        DELETE FROM event_logs WHERE event_id = %s
        """
        for row in rows:
            self.session.execute(delete_query, (row.event_id,))
            self.logger.info(['cassandra', 'old_event_deleted'], event_id=row.event_id)

    def export_data_to_json(self):
        """
        Експортує всі дані з таблиці логів подій у JSON файл.
        """
        rows = self.session.execute("SELECT * FROM event_logs")
        data = [{'event_id': str(row.event_id),
                 'user_id': str(row.user_id),
                 'event_type': row.event_type,
                 'timestamp': str(row.timestamp),
                 'metadata': row.metadata} for row in rows]
        with open('cassandra_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        self.logger.info(['cassandra', 'data_exported'])


if __name__ == "__main__":
    with EventLogManager("127.0.0.1", 9042, "your_keyspace", "cassandra", "cassandra") as manager:
        # Створення таблиці
        manager.create_event_log_table()

        # Додавання подій
        manager.create_event_log(user_id=uuid.uuid4(), event_type='login', metadata='User logged in successfully')

        # Отримання подій за типом за останні 24 години
        events = manager.read_events_by_type('login')
        for event in events:
            print(f"Event: {event.event_id}, Metadata: {event.metadata}")

        # Оновлення метаданих події
        manager.update_event_metadata(event_id=events[0].event_id, new_metadata="Updated metadata")

        # Видалення старих подій
        manager.delete_old_events()

        # Експорт даних у JSON
        manager.export_data_to_json()



# Cassandra забезпечує надійність завдяки реплікації даних на кількох серверах. Якщо один сервер виходить
# з ладу, інші зберігають копії. Масштабування досягається додаванням нових серверів у кластер,
# що дозволяє обробляти більше даних і запитів без зупинки роботи.
