import math

class Vector:
    """
    Клас Vector для представлення вектора в n-вимірному просторі.

    Атрибути:
    ----------
    coordinates : tuple
        Координати вектора у вигляді кортежу.
    """

    def __init__(self, *coordinates):
        """
        Ініціалізує екземпляр класу Vector з будь-якою кількістю координат.

        :param coordinates: Координати вектора (float).
        """
        self.coordinates = coordinates

    def __add__(self, other):
        """
        Додає два вектори.

        :param other: Інший екземпляр класу Vector.
        :return: Новий екземпляр класу Vector, що є сумою двох векторів.
        :raises ValueError: Якщо кількість координат у векторах не збігається.
        """
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Вектори повинні мати однакову кількість вимірів.")
        result = tuple(a + b for a, b in zip(self.coordinates, other.coordinates))
        return Vector(*result)

    def __sub__(self, other):
        """
        Віднімає один вектор від іншого.

        :param other: Інший екземпляр класу Vector.
        :return: Новий екземпляр класу Vector, що є різницею двох векторів.
        :raises ValueError: Якщо кількість координат у векторах не збігається.
        """
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Вектори повинні мати однакову кількість вимірів.")
        result = tuple(a - b for a, b in zip(self.coordinates, other.coordinates))
        return Vector(*result)

    def __mul__(self, other):
        """
        Обчислює скалярний добуток двох векторів.

        :param other: Інший екземпляр класу Vector.
        :return: Скалярний добуток двох векторів (float).
        :raises ValueError: Якщо кількість координат у векторах не збігається.
        """
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Вектори повинні мати однакову кількість вимірів.")
        return sum(a * b for a, b in zip(self.coordinates, other.coordinates))

    def magnitude(self):
        """
        Обчислює довжину (модуль) вектора.

        :return: Довжина вектора (float).
        """
        return math.sqrt(sum(x**2 for x in self.coordinates))

    def __len__(self):
        """
        Повертає кількість вимірів вектора.

        :return: Кількість вимірів вектора (int).
        """
        return len(self.coordinates)

    def __lt__(self, other):
        """
        Порівнює довжину поточного вектора з іншим вектором.

        :param other: Інший екземпляр класу Vector.
        :return: True, якщо довжина поточного вектора менша за інший вектор (bool).
        """
        return self.magnitude() < other.magnitude()

    def __le__(self, other):
        """
        Порівнює довжину поточного вектора з іншим вектором.

        :param other: Інший екземпляр класу Vector.
        :return: True, якщо довжина поточного вектора менша або рівна іншому вектору (bool).
        """
        return self.magnitude() <= other.magnitude()

    def __eq__(self, other):
        """
        Порівнює довжину поточного вектора з іншим вектором.

        :param other: Інший екземпляр класу Vector.
        :return: True, якщо довжини векторів рівні (bool).
        """
        return self.magnitude() == other.magnitude()

    def __repr__(self):
        """
        Повертає текстове представлення вектора.

        :return: Текстове представлення вектора (str).
        """
        return f"Vector{self.coordinates}"


# Приклад використання
v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

# Додавання
v3 = v1 + v2
print(f"Додавання векторів: {v3}")

# Віднімання
v4 = v1 - v2
print(f"Віднімання векторів: {v4}")

# Скалярний добуток
dot_product = v1 * v2
print(f"Скалярний добуток: {dot_product}")

# Порівняння за довжиною
print(f"v1 < v2: {v1 < v2}")
print(f"v1 == v2: {v1 == v2}")
print(f"v1 > v2: {v1 > v2}")
