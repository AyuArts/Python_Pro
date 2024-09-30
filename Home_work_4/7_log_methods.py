import logging.config

# Чтение и применение конфигурации из файла
logging.config.fileConfig('logging.conf')

# Получаем настроенный логер
logger = logging.getLogger('my_logger')


def log_methods(cls):
    """
    Декоратор класу, що логуватиме виклики всіх методів цього класу.

    :param cls: Клас, методи якого потрібно логувати.
    :return: Клас з логуванням методів.
    """
    # Проходимо по всіх атрибутах класу
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith('__'):
            # Декоруємо кожен метод класу
            setattr(cls, attr_name, log_method(attr_value))
    return cls


def log_method(method):
    """
    Декоратор для логування виклику методу.

    :param method: Метод, який потрібно логувати.
    :return: Обгорнутий метод з логуванням.
    """

    def wrapper(*args, **kwargs):
        logging.info(f"Logging: {method.__name__} called with {args[1:]}, {kwargs}")
        return method(*args, **kwargs)

    return wrapper


# Приклад використання
@log_methods
class MyClass:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


# Створюємо об'єкт класу
obj = MyClass()

# Викликаємо методи
obj.add(5, 3)  # Логування: add called with (5, 3)
obj.subtract(5, 3)  # Логування: subtract called with (5, 3)
