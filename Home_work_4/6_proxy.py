import logging.config

# Чтение и применение конфигурации из файла
logging.config.fileConfig('logging.conf')

# Получаем настроенный логер
logger = logging.getLogger('my_logger')


class Proxy:
    def __init__(self, obj):
        """
        Ініціалізує проксі-об'єкт, що приймає оригінальний об'єкт для перехоплення методів.

        :param obj: Об'єкт, методи якого будуть перехоплюватися.
        """
        self._obj = obj  # Зберігаємо оригінальний об'єкт

    def __getattr__(self, name):
        """
        Перехоплює доступ до атрибутів і методів оригінального об'єкта.

        :param name: Назва методу або атрибуту.
        :return: Власне значення атрибуту або обгортку для методів.
        """
        # Отримуємо атрибут або метод оригінального об'єкта
        attr = getattr(self._obj, name)

        if callable(attr):
            # Якщо це метод, то повертаємо функцію-обгортку, що логуватиме виклики
            def wrapper(*args, **kwargs):
                logging.info(f"Calling method: {name} with args: {args}, kwargs: {kwargs}")
                result = attr(*args, **kwargs)
                return result

            return wrapper
        else:
            # Якщо це не метод, а атрибут, повертаємо його значення
            return attr


# Приклад використання
class MyClass:
    def greet(self, name):
        return f"Hello, {name}!"


# Створюємо оригінальний об'єкт
obj = MyClass()

# Створюємо проксі-об'єкт
proxy = Proxy(obj)

# Викликаємо метод через проксі
print(proxy.greet("Alice"))  # Лог: Calling method: greet with args: ('Alice',)