# matrix_operations.py

from typing import List


def matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
    """
    Множить дві матриці.

    :param matrix1: Перша матриця для множення.
    :type matrix1: List[List[int]]
    :param matrix2: Друга матриця для множення.
    :type matrix2: List[List[int]]
    :return: Результуюча матриця після множення.
    :rtype: List[List[int]]
    :raises ValueError: Якщо матриці порожні або кількість стовпців першої матриці не дорівнює кількості рядків другої.

    :example:
    >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]

    >>> matrix_multiply([[2, 0], [1, 2]], [[3, 4], [5, 6]])
    [[6, 8], [13, 16]]

    >>> matrix_multiply([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]])
    [[58, 64], [139, 154]]

    >>> matrix_multiply([[1]], [[1]])
    [[1]]
    """
    if not matrix1 or not matrix2:
        raise ValueError("Матриці не можуть бути порожніми.")

    num_rows_m1, num_cols_m1 = len(matrix1), len(matrix1[0])
    num_rows_m2, num_cols_m2 = len(matrix2), len(matrix2[0])

    if num_cols_m1 != num_rows_m2:
        raise ValueError("Кількість стовпців першої матриці повинна дорівнювати кількості рядків другої.")

    result = []
    for i in range(num_rows_m1):
        result_row = []
        for j in range(num_cols_m2):
            sum_product = 0
            for k in range(num_cols_m1):
                sum_product += matrix1[i][k] * matrix2[k][j]
            result_row.append(sum_product)
        result.append(result_row)
    return result


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Транспонує матрицю.

    :param matrix: Матриця для транспонування.
    :type matrix: List[List[int]]
    :return: Транспонована матриця.
    :rtype: List[List[int]]
    :raises ValueError: Якщо матриця порожня.

    :example:
    >>> transpose_matrix([[1, 2], [3, 4]])
    [[1, 3], [2, 4]]

    >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]

    >>> transpose_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    >>> transpose_matrix([[1]])
    [[1]]
    """
    if not matrix:
        raise ValueError("Матриця не може бути порожньою.")
    return list(map(list, zip(*matrix)))
