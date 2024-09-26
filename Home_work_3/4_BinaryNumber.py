class BinaryNumber:
    """
    Клас для представлення двійкових чисел і виконання бітових операцій
    над ними, таких як AND, OR, XOR та інверсія (NOT).
    """

    def __init__(self, value):
        """
        Ініціалізує двійкове число з рядка або цілого числа.

        :param value: Двійкове число у вигляді рядка (str) або десяткового числа (int).
        :raises TypeError: Якщо значення не є рядком або цілим числом.
        """
        if isinstance(value, str):
            # Перетворюємо двійковий рядок у ціле число
            self.value = int(value, 2)
        elif isinstance(value, int):
            self.value = value
        else:
            raise TypeError("Value must be a binary string or integer.")

    def __and__(self, other):
        """
        Операція AND над двома двійковими числами.

        :param other: Інший екземпляр класу BinaryNumber.
        :return: Новий екземпляр класу BinaryNumber після виконання операції AND.
        """
        return BinaryNumber(self.value & other.value)

    def __or__(self, other):
        """
        Операція OR над двома двійковими числами.

        :param other: Інший екземпляр класу BinaryNumber.
        :return: Новий екземпляр класу BinaryNumber після виконання операції OR.
        """
        return BinaryNumber(self.value | other.value)

    def __xor__(self, other):
        """
        Операція XOR над двома двійковими числами.

        :param other: Інший екземпляр класу BinaryNumber.
        :return: Новий екземпляр класу BinaryNumber після виконання операції XOR.
        """
        return BinaryNumber(self.value ^ other.value)

    def __invert__(self):
        """
        Операція інверсії (NOT) над двійковим числом.

        :return: Новий екземпляр класу BinaryNumber після виконання операції NOT.
        """
        # Ми повертаємо інверсію, використовуючи маску на 32 біти
        mask = (1 << self.value.bit_length()) - 1
        return BinaryNumber(~self.value & mask)

    def __repr__(self):
        """
        Повертає строкове представлення двійкового числа у форматі бінарного рядка.

        :return: Бінарне представлення двійкового числа (str) з додатковими нулями.
        """
        bit_length = max(4, self.value.bit_length())  # Встановлюємо мінімальну довжину 4 біти
        return format(self.value, f'0{bit_length}b')


# Тестування
def test_binary_operations():
    """
    Функція для тестування основних бітових операцій між двійковими числами.

    :raises AssertionError: Якщо один із тестів не проходить.
    """
    num1 = BinaryNumber("1010")  # 10 у десятковій системі
    num2 = BinaryNumber("1100")  # 12 у десятковій системі

    # Тест операції AND
    assert (num1 & num2).__repr__() == "1000", f"Помилка в AND: {num1 & num2}"
    print("AND:", num1 & num2)  # Має бути 1000 (8)

    # Тест операції OR
    assert (num1 | num2).__repr__() == "1110", f"Помилка в OR: {num1 | num2}"
    print("OR:", num1 | num2)  # Має бути 1110 (14)

    # Тест операції XOR
    assert (num1 ^ num2).__repr__() == "0110", f"Помилка в XOR: {num1 ^ num2}"
    print("XOR:", num1 ^ num2)  # Має бути 0110 (6)

    # Тест операції NOT для num1
    assert (~num1).__repr__() == "0101", f"Помилка в NOT: {~num1}"
    print("NOT:", ~num1)  # Має бути 0101 (5) для інверсії 1010


# Виклик тестів
test_binary_operations()
