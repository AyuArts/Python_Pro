# Task 6

def create_calculator(operator):
    """
    Створює калькулятор для виконання математичних операцій.

    Аргументи:
    operator (str): Оператор для обчислення ('+', '-', '*', '/').

    Повертає:
    function: Функцію для обчислення значень.
    """
    value_x = "x"
    value_y = "y"

    def numeric_values(x, y):
        """
        Виконує обчислення між двома значеннями.

        Аргументи:
        x (int/float): Перше число.
        y (int/float): Друге число.

        Повертає:
        str: Результат обчислення або повідомлення про помилку.
        """
        nonlocal value_x, value_y

        value_x = x
        value_y = y
        calculator = f"{value_x} {operator} {value_y}"

        if operator == '/':
            if y != 0:
                result = f"{calculator} = {eval(calculator)}"
                return result
            else:
                return f"{calculator} = Помилка: Ділення на нуль"
        elif operator in ['+', '-', '*']:
            result = f"{calculator} = {eval(calculator)}"
            return result
        else:
            return "Невідомий оператор"

    print(f"{value_x} {operator} {value_y}")

    return numeric_values


print(create_calculator("/")(1, 0))
