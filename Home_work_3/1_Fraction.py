import math


class Fraction:
    """
    Клас для представлення і роботи з дробами.
    Підтримує операції додавання, віднімання, множення і ділення дробів.
    """

    def __init__(self, numerator, denominator):
        """
        Ініціалізує екземпляр класу Fraction.

        :param numerator: Чисельник дробу (int).
        :param denominator: Знаменник дробу (int). Не може бути рівним нулю.
        :raises ValueError: Якщо знаменник дорівнює нулю.
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def simplify(self):
        """
        Скорочує дріб за допомогою найбільшого спільного дільника (НСД).
        Модифікує чисельник і знаменник дробу.
        """
        gcd = math.gcd(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    def __add__(self, other):
        """
        Додає два дроби.

        :param other: Інший екземпляр класу Fraction.
        :return: Новий екземпляр класу Fraction, що є сумою двох дробів.
        """
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __sub__(self, other):
        """
        Віднімає один дріб від іншого.

        :param other: Інший екземпляр класу Fraction.
        :return: Новий екземпляр класу Fraction, що є різницею двох дробів.
        """
        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __mul__(self, other):
        """
        Множить два дроби.

        :param other: Інший екземпляр класу Fraction.
        :return: Новий екземпляр класу Fraction, що є добутком двох дробів.
        """
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __truediv__(self, other):
        """
        Ділить один дріб на інший.

        :param other: Інший екземпляр класу Fraction.
        :return: Новий екземпляр класу Fraction, що є часткою двох дробів.
        :raises ValueError: Якщо чисельник іншого дробу дорівнює нулю.
        """
        if other.numerator == 0:
            raise ValueError("Cannot divide by zero.")
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)

    def __repr__(self):
        """
        Повертає строкове представлення дробу у форматі numerator/denominator.

        :return: Строкове представлення дробу (str).
        """
        return f"{self.numerator}/{self.denominator}"


# Приклад використання:
frac1 = Fraction(1, 2)
frac2 = Fraction(3, 4)

print(frac1 + frac2)  # Виведе: 5/4
print(frac1 - frac2)  # Виведе: -1/4
print(frac1 * frac2)  # Виведе: 3/8
print(frac1 / frac2)  # Виведе: 2/3
