import doctest

def is_even(n: int) -> bool:
    """
    Перевіряє, чи є число парним.

    Параметри:
    n (int): Ціле число для перевірки.

    Повертає:
    bool: True, якщо число парне, і False, якщо непарне.

    >>> is_even(2)
    True
    >>> is_even(3)
    False
    """
    return n % 2 == 0


def factorial(n):
    """
    Обчислює факторіал числа n.

    Параметри:
    n (int): Ціле число, факторіал якого потрібно обчислити.

    Повертає:
    int: Факторіал числа n.

    >>> factorial(5)
    120
    >>> factorial(0)
    1
    >>> factorial(1)
    1
    """
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


if __name__ == "__main__":
    doctest.testmod()
