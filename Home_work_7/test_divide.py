import pytest

def divide(a: int, b: int) -> float:
    """
    Виконує ділення числа a на b.


    :param a (int): Дільник.
    :param b (int): Дільник.


    :return float: Результат ділення a на b.


    :except ZeroDivisionError: Якщо b дорівнює нулю, виводиться відповідне повідомлення.
    """
    if b == 0:
        raise ZeroDivisionError("Ділення на нуль неможливе.")
    return a / b


def test_divide_correct():
    """
    Перевіряє коректний поділ двох чисел.
    """
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(-9, 3) == -3.0


def test_divide_zero_division():
    """
    Перевіряє, що викликається ZeroDivisionError при діленні на нуль.
    """
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  # Переконуємося, що ZeroDivisionError викликано


if __name__ == "__main__":
    pytest.main()
