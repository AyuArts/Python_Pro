from decimal import Decimal, ROUND_HALF_UP


class Price:
    """
    Клас для представлення ціни товару з можливістю виконання основних
    операцій над цінами, таких як додавання, віднімання та порівняння.
    """

    def __init__(self, amount):
        """
        Ініціалізує екземпляр класу Price.

        :param amount: Числове значення ціни (float або Decimal).
        """
        self.amount = self._round_price(amount)

    @staticmethod
    def _round_price(amount):
        """
        Заокруглює ціну до двох десяткових знаків.

        :param amount: Числове значення ціни.
        :return: Заокруглене значення ціни.
        """
        return Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __add__(self, other):
        """
        Додає дві ціни.

        :param other: Інший екземпляр класу Price.
        :return: Новий екземпляр класу Price з доданою ціною.
        """
        return Price(self.amount + other.amount)

    def __sub__(self, other):
        """
        Віднімає одну ціну від іншої.

        :param other: Інший екземпляр класу Price.
        :return: Новий екземпляр класу Price з віднятою ціною.
        """
        return Price(self.amount - other.amount)

    def __eq__(self, other):
        """
        Порівнює дві ціни на рівність.

        :param other: Інший екземпляр класу Price.
        :return: True, якщо ціни рівні, інакше False.
        """
        return self.amount == other.amount

    def __lt__(self, other):
        """
        Порівнює дві ціни (менше).

        :param other: Інший екземпляр класу Price.
        :return: True, якщо поточна ціна менша, інакше False.
        """
        return self.amount < other.amount

    def __le__(self, other):
        """
        Порівнює дві ціни (менше або дорівнює).

        :param other: Інший екземпляр класу Price.
        :return: True, якщо поточна ціна менша або рівна, інакше False.
        """
        return self.amount <= other.amount

    def __repr__(self):
        """
        Повертає строкове представлення ціни.

        :return: Строкове значення ціни.
        """
        return f"Price({self.amount})"


def test_advanced_price_operations():
    # Тест на граничні випадки
    print("=== Тест на граничні випадки ===")
    price_zero = Price(0)
    price_small = Price(0.004)
    price_large = Price(999999999.99)

    print(f"Ціна 0: {price_zero}")  # Очікується: Price(0.00)
    print(f"Маленька ціна: {price_small}")  # Очікується: Price(0.00)
    print(f"Велика ціна: {price_large}")  # Очікується: Price(999999999.99)

    # Тест операцій з кількома цінами
    print("=== Тест операцій з кількома цінами ===")
    price1 = Price(19.99)
    price2 = Price(10.50)
    price3 = Price(5.75)

    total_price = price1 + price2 + price3
    print(f"Сума трьох цін: {total_price}")  # Очікується: Price(36.24)

    # Тест на віднімання
    print("=== Тест на віднімання ===")
    difference_price = price1 - price3
    print(f"Різниця між ціною 1 і ціною 3: {difference_price}")  # Очікується: Price(14.24)

    # Тест на від’ємні результати
    print("=== Тест на від’ємні результати ===")
    negative_price = price2 - price1
    print(f"Від’ємна ціна: {negative_price}")  # Очікується: Price(-9.49)

    # Тест на порівняння
    print("=== Тест на порівняння ===")
    print(f"Ціна 1 дорівнює ціні 2: {price1 == price2}")  # Очікується: False
    print(f"Ціна 1 більше ціни 3: {price1 > price3}")  # Очікується: True
    print(f"Ціна 2 менше або дорівнює ціні 3: {price2 <= price3}")  # Очікується: False
    print(f"Ціна 3 менше ціни 1: {price3 < price1}")  # Очікується: True

    # Тест на роботу з десятковими знаками
    print("=== Тест на заокруглення ===")
    price_round_test1 = Price(1.005)
    price_round_test2 = Price(2.555)
    print(f"Ціна з заокругленням 1.005: {price_round_test1}")  # Очікується: Price(1.01)
    print(f"Ціна з заокругленням 2.555: {price_round_test2}")  # Очікується: Price(2.56)

    # Тест з груповими операціями (список цін)
    print("=== Тест з груповими операціями ===")
    prices = [Price(9.99), Price(14.99), Price(4.50), Price(29.95)]
    total_group_price = sum(prices, Price(0))  # Використовуємо Price(0) як початкову точку
    print(f"Загальна сума групи цін: {total_group_price}")  # Очікується: Price(59.43)

    # Тест з некоректними даними
    print("=== Тест з некоректними даними ===")
    try:
        invalid_price = Price("abc")
    except Exception as e:
        print(f"Викинуто виняток: {e}")  # Очікується: Виняток через некоректний формат даних


# Викликаємо функцію тестування
test_advanced_price_operations()
