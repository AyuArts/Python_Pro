def factorial_search(number: int) -> int:
    """
    Обчислює факторіал заданого числа.

    :param number: Ціле додатне число, для якого потрібно знайти факторіал.
    :return: Факторіал числа.
    """
    factorial = 1
    # Цикл для множення всіх чисел від 1 до number включно
    for x in range(1, number + 1):
        factorial *= x
    return factorial


def nod_search(x: int, y: int) -> int:
    """
    Знаходить найбільший спільний дільник (НСД) двох чисел за допомогою алгоритму Евкліда.

    :param x: Перше ціле число.
    :param y: Друге ціле число.
    :return: Найбільший спільний дільник двох чисел.
    """
    # Алгоритм Евкліда для пошуку НСД
    while y != 0:
        x, y = y, x % y
    return x
