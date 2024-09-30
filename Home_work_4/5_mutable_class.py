import logging.config

# Чтение и применение конфигурации из файла
logging.config.fileConfig('logging.conf')

# Получаем настроенный логер
logger = logging.getLogger('my_logger')

class MutableClass:
    """
    Клас для динамічного додавання, зміни та видалення атрибутів об'єкта під час виконання.
    """

    def __init__(self):
        """Ініціалізує екземпляр класу без додаткових атрибутів."""
        pass


    def validate_name(self, name):
        """
        Перевіряє, що назва атрибуту є рядком. Якщо це не так, логує помилку.

        :param name: Назва атрибуту.
        :return: True, якщо назва є рядком, інакше False.
        """
        if not isinstance(name, str):
            logger.error("Назва атрибуту повинна бути рядком.")
            return False
        return True

    def set_attribute(self, name, value):
        """
        Додає новий атрибут або оновлює значення існуючого.

        :param name: Назва атрибуту.
        :param value: Значення атрибуту.
        """
        if not self.validate_name(name):
            return

        action = 'доданий' if not hasattr(self, name) else 'оновлений'
        setattr(self, name, value)
        logger.info(f"Атрибут '{name}' був {action} зі значенням '{value}'.")

    def get_attribute(self, name):
        """
        Повертає значення атрибуту, якщо він існує.

        :param name: Назва атрибуту.
        :return: Значення атрибуту або None.
        """
        if not self.validate_name(name):
            return None

        if hasattr(self, name):
            value = getattr(self, name)
            logger.info(f"{name} = '{value}'.")
            return value

        logger.warning(f"Атрибут '{name}' відсутній.")
        return None

    def delete_attribute(self, name):
        """
        Видаляє атрибут, якщо він існує.

        :param name: Назва атрибуту.
        """
        if not self.validate_name(name):
            return

        if hasattr(self, name):
            delattr(self, name)
            logger.info(f"Атрибут '{name}' був видалений.")
        else:
            logger.warning(f"Атрибут '{name}' не існує.")


# Приклад використання
if __name__ == "__main__":
    obj = MutableClass()

    # Додаємо атрибут
    obj.set_attribute("name", "Python")  # Логування: Атрибут 'name' був доданий зі значенням 'Python'.

    # Отримуємо значення атрибуту
    obj.get_attribute("name")  # Логування: Атрибут 'name' має значення 'Python'.

    # Змінюємо атрибут
    obj.set_attribute("name", "Java")  # Логування: Атрибут 'name' був оновлений зі значенням 'Java'.

    # Отримуємо оновлене значення атрибуту
    obj.get_attribute("name")  # Логування: Атрибут 'name' має значення 'Java'.

    # Видаляємо атрибут
    obj.delete_attribute("name")  # Логування: Атрибут 'name' був видалений.

    # Прагнемо отримати значення видаленого атрибуту
    obj.get_attribute("name")  # Логування: Атрибут 'name' відсутній.






    