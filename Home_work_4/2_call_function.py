from tomlkit import document


def call_function(obj, method_name, *args):
    """
    Викликає метод об'єкта за його назвою та переданими аргументами.

    :param obj: Об'єкт, метод якого потрібно викликати
    :param method_name: Назва методу у вигляді рядка
    :param args: Довільні аргументи для методу
    :return: Результат виконання методу
    """
    # Отримуємо метод з об'єкта за назвою
    method = getattr(obj, method_name)
    # Викликаємо метод з переданими аргументами
    return method(*args)


# Приклад використання
class Calculator:
    """
    Клас калькулятора з методами додавання та віднімання.
    """

    def add(self, a, b):
        """
        Додає два числа.

        :param a: Перше число
        :param b: Друге число
        :return: Сума a та b
        """
        return a + b

    def subtract(self, a, b):
        """
        Віднімає друге число від першого.

        :param a: Перше число
        :param b: Друге число
        :return: Різниця a та b
        """
        return a - b



calc = Calculator()
print(call_function(calc, "add", 10, 5))       # 15
print(call_function(calc, "subtract", 10, 5))  # 5
