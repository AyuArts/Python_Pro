import logging.config

# Читання і застосування конфігурації з файлу
logging.config.fileConfig('logging.conf')

# Отримуємо налаштований логер
logger = logging.getLogger('my_logger')


class SingletonMeta(type):
    """
    Метаклас SingletonMeta гарантує, що кожен клас, який використовує цей метаклас, матиме лише один екземпляр.
    Всі наступні спроби створити новий екземпляр будуть повертати вже існуючий об'єкт.

    Атрибути:
        _instances (dict): Словник, що зберігає екземпляри класів, для контролю одночасно створених об'єктів.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Викликається при створенні екземпляра класу. Якщо екземпляр класу вже створено, повертається
        раніше створений екземпляр. Інакше створюється новий екземпляр і зберігається.

        :param cls: Клас, для якого створюється екземпляр.
        :param args: Додаткові позиційні аргументи для ініціалізації класу.
        :param kwargs: Додаткові іменовані аргументи для ініціалізації класу.
        :return: Повертає екземпляр класу.
        :rtype: object
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Клас Singleton використовує метаклас SingletonMeta для гарантії, що він матиме лише один екземпляр.

    Атрибути:
        Не має специфічних атрибутів на рівні екземпляра.
    """

    def __init__(self):
        """
        Ініціалізує екземпляр класу Singleton. Логерується факт створення екземпляра.
        """
        logger.info("Creating instance")


# Створення екземплярів класу Singleton
obj1 = Singleton()  # Створюється перший екземпляр
obj2 = Singleton()  # Повертається той самий екземпляр

# Перевірка, чи обидва об'єкти вказують на один і той самий екземпляр
logger.info(f"obj1 is obj2: {obj1 is obj2}")  # True
