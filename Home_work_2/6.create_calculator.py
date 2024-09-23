# Task 6 ==============================================

def create_calculator(operator):
    value_x = "x"
    value_y = "y"


    def numeric_values(x, y):
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
        elif operator in ['+', '-', '*',]:
            result = f"{calculator} = {eval(calculator)}"
            return result
        else:
            return "Невідомий оператор"

    print(f"{value_x} {operator} {value_y}")

    return numeric_values


print(create_calculator("/")(1,0))
