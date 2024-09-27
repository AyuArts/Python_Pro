import math


class Vector:
    """
    Клас для представлення вектора у просторі з можливістю виконання
    базових операцій, таких як додавання, віднімання, множення на скаляр
    та порівняння векторів за довжиною.
    """

    def __init__(self, *components):
        """
        Ініціалізує екземпляр класу Vector.

        :param components: Компоненти вектора (координати), передаються через аргументи.
        """
        self.components = components

    def __add__(self, other):
        """
        Додає два вектори.

        :param other: Інший екземпляр класу Vector.
        :return: Новий екземпляр класу Vector, що є сумою двох векторів.
        :raises ValueError: Якщо вектори мають різні розміри.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must be of the same dimension.")
        result = [a + b for a, b in zip(self.components, other.components)]
        return Vector(*result)

    def __sub__(self, other):
        """
        Віднімає один вектор від іншого.

        :param other: Інший екземпляр класу Vector.
        :return: Новий екземпляр класу Vector, що є різницею двох векторів.
        :raises ValueError: Якщо вектори мають різні розміри.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must be of the same dimension.")
        result = [a - b for a, b in zip(self.components, other.components)]
        return Vector(*result)

    def __mul__(self, scalar):
        """
        Множить вектор на скаляр.

        :param scalar: Число, на яке потрібно помножити вектор.
        :return: Новий екземпляр класу Vector, що є добутком вектора і скаляра.
        """
        result = [a * scalar for a in self.components]
        return Vector(*result)

    def __eq__(self, other):
        """
        Порівнює вектори за їх довжиною (на рівність).

        :param other: Інший екземпляр класу Vector.
        :return: True, якщо довжини векторів рівні, інакше False.
        """
        return self.length() == other.length()

    def __lt__(self, other):
        """
        Порівнює вектори за їх довжиною (менше).

        :param other: Інший екземпляр класу Vector.
        :return: True, якщо довжина поточного вектора менша, інакше False.
        """
        return self.length() < other.length()

    def length(self):
        """
        Обчислює довжину (модуль) вектора.

        :return: Довжина вектора (float).
        """
        return math.sqrt(sum(a ** 2 for a in self.components))

    def __repr__(self):
        """
        Повертає строкове представлення вектора.

        :return: Строкове представлення вектора (str).
        """
        return f"Vector{self.components}"


# Приклад використання:
v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

print(v1 + v2)  # Додавання: Vector(5, 7, 9)
print(v1 - v2)  # Віднімання: Vector(-3, -3, -3)
print(v1 * 3)  # Множення на число: Vector(3, 6, 9)
print(v1.length())  # Довжина вектора: 3.7416573867739413
print(v1 == v2)  # Порівняння: False
print(v1 < v2)  # Порівняння за довжиною: True
