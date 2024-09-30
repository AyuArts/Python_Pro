import inspect
import logging.config

# Чтение и применение конфигурации из файла
logging.config.fileConfig('logging.conf')

# Получаем настроенный логер
logger = logging.getLogger('my_logger')


def get_methods(cls):
    """
    Получает список названий методов класса.

    :param cls: Класс для анализа.
    :return: Список названий методов (list).
    """
    methods = []  # Инициализируем список для хранения названий методов

    # Получаем все методы класса, используя inspect.getmembers
    for name, attr in inspect.getmembers(cls, predicate=inspect.isfunction):
        methods.append(name)  # Добавляем имя метода в список

    return methods  # Возвращаем список методов


def analyze_inheritance(cls):
    """
    Анализирует класс и его наследование, извлекая информацию о методах текущего класса и его родительских классов.
    :param cls: Класс для анализа. Ожидается, что он может иметь батьківські класи (type).
    :return: None. Информация о методах класса и его наследовании записывается в лог.
    """
    # Отримуємо назву класу
    class_name = cls.__name__

    # Отримуємо назви батьківських класів та їх методи
    methods_bases = []
    name_bases = []

    for base_class in cls.__bases__:
        name_bases.append(base_class.__name__)  # Додаємо назву батьківського класу
        base_methods = get_methods(base_class)  # Отримуємо методи батьківського класу
        for name in base_methods:
            methods_bases.append(f"{name}")  # Форматуємо назви методів

    # Отримуємо методи поточного класу
    methods_class = get_methods(cls)

    # Логування інформації про клас і його наслідування
    logger.info(f"інформація про клас і його наслідування"
                f"\n{"-" * 46}"
                f"\nИмя класа: {class_name}"
                f"\nЙого методи: {', '.join(methods_class)}"
                f"\nНаслідує: {', '.join(methods_bases)}"
                f" з {', '.join(name_bases)}")


class Parent:
    def parent_method(self):
        pass


class Child(Parent):
    def child_method(self):
        pass


analyze_inheritance(Child)
