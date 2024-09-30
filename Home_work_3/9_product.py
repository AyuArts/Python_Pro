class PriceDescriptor:
    """
    Клас PriceDescriptor є дескриптором, який контролює отримання та встановлення ціни товару в базовій валюті (гривні).

    Методи:
    -------
    __get__(instance, owner) -> float:
        Повертає значення ціни товару.
    __set__(instance, value: float) -> None:
        Встановлює значення ціни з перевіркою на від'ємне значення.
    """

    def __get__(self, instance, owner) -> float:
        """
        Повертає ціну товару.

        :param instance: Екземпляр класу ProductWithDescriptor.
        :param owner: Клас власника дескриптора.
        :return: Ціна товару (float).
        """
        return instance._price

    def __set__(self, instance, value: float) -> None:
        """
        Встановлює ціну товару з перевіркою на від'ємне значення.

        :param instance: Екземпляр класу ProductWithDescriptor.
        :param value: Нова ціна товару (float).
        :raises ValueError: Якщо ціна є від'ємною.
        """
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        instance._price = value


class CurrencyDescriptor:
    """
    Клас CurrencyDescriptor конвертує ціну між різними валютами.

    Методи:
    -------
    __get__(instance, owner) -> float:
        Повертає значення ціни в обраній валюті.
    __set__(instance, value: tuple) -> None:
        Встановлює значення ціни в іншій валюті.
    """

    exchange_rates = {
        'EUR': 40.0,  # Курс гривня до євро
        'USD': 36.5  # Курс гривня до долара
    }

    def __get__(self, instance, owner) -> float:
        """
        Повертає ціну товару в обраній валюті.

        :param instance: Екземпляр класу ProductWithDescriptor.
        :param owner: Клас власника дескриптора.
        :return: Ціна товару в валюті (float).
        """
        price_in_uah = instance._price
        return price_in_uah / self.exchange_rates[instance.currency]

    def __set__(self, instance, value: tuple) -> None:
        """
        Встановлює ціну товару в іншій валюті.

        :param instance: Екземпляр класу ProductWithDescriptor.
        :param value: Кортеж у вигляді (нова ціна, валюта).
        :raises ValueError: Якщо ціна є від'ємною.
        """
        amount, currency = value
        if amount < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        if currency not in self.exchange_rates:
            raise ValueError(f"Невідома валюта: {currency}")

        instance._price = amount * self.exchange_rates[currency]
        instance.currency = currency


class ProductWithDescriptor:
    """
    Клас ProductWithDescriptor представляє товар з використанням дескриптора для управління ціною та її конвертації.

    Атрибути:
    ----------
    name : str
        Назва товару.
    price : float
        Ціна товару в базовій валюті (гривня).
    currency : str
        Валюта, в якій представлена ціна товару (гривня, долар або євро).
    """

    price = PriceDescriptor()  # Основна ціна у гривнях
    price_in_currency = CurrencyDescriptor()  # Ціна в іншій валюті

    def __init__(self, name: str, price: float, currency: str = 'UAH'):
        """
        Ініціалізує товар з іменем, ціною та валютою.

        :param name: Назва товару (str).
        :param price: Ціна товару (float).
        :param currency: Валюта товару (str, за замовчуванням 'UAH').
        :raises ValueError: Якщо ціна є від'ємною.
        """
        self.name = name
        self.currency = currency
        self.price = price


class ProductWithGetSet:
    """
    Клас ProductWithGetSet представляє товар з можливістю отримувати та встановлювати
    ціну через методи get_price і set_price.

    Атрибути:
    ----------
    name : str
        Назва товару.
    price : float
        Ціна товару (не може бути від'ємною).
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.set_price(price)

    def get_price(self) -> float:
        """Повертає ціну товару."""
        return self._price

    def set_price(self, value: float) -> None:
        """Встановлює ціну з перевіркою на від'ємне значення."""
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        self._price = value


class ProductWithProperty:
    """
    Клас ProductWithProperty представляє товар з використанням декоратора @property для управління ціною.

    Атрибути:
    ----------
    name : str
        Назва товару.
    price : float
        Ціна товару (не може бути від'ємною).
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @property
    def price(self) -> float:
        """Повертає ціну товару."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Встановлює ціну з перевіркою на від'ємне значення."""
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        self._price = value


# Тестова програма
def test_products_with_currency():
    """
    Тестує реалізацію дескрипторів для управління ціною в різних валютах.

    :raises ValueError: Якщо будь-яка з реалізацій ціни порушує умови перевірки.
    """
    # Тестування дескриптора з ціною в гривнях
    try:
        product = ProductWithDescriptor("Товар 1", 1000)
        print(f"ProductWithDescriptor: {product.price} грн")

        # Зміна ціни в доларах
        product.price_in_currency = (30, 'USD')
        print(f"Price in USD: {product.price_in_currency} USD")

        # Зміна ціни в євро
        product.price_in_currency = (25, 'EUR')
        print(f"Price in EUR: {product.price_in_currency} EUR")

        # Спроба встановити від'ємну ціну
        product.price_in_currency = (-10, 'EUR')
    except ValueError as e:
        print(f"Error in ProductWithDescriptor: {e}")


def test_products():
    """
    Тестує три реалізації роботи з ціною: через методи, @property і дескриптор.

    :raises ValueError: Якщо будь-яка з реалізацій ціни порушує умови перевірки.
    """
    # Тестування сеттерів/геттерів
    try:
        product1 = ProductWithGetSet("Товар 1", 50)
        print(f"ProductWithGetSet: {product1.get_price()}")
        product1.set_price(100)
        print(f"Updated Price (set_price): {product1.get_price()}")
        product1.set_price(-10)
    except ValueError as e:
        print(f"Error in ProductWithGetSet: {e}")

    # Тестування @property
    try:
        product2 = ProductWithProperty("Товар 2", 75)
        print(f"ProductWithProperty: {product2.price}")
        product2.price = 150
        print(f"Updated Price (property): {product2.price}")
        product2.price = -20
    except ValueError as e:
        print(f"Error in ProductWithProperty: {e}")

    # Тестування дескриптора
    try:
        product3 = ProductWithDescriptor("Товар 3", 200)
        print(f"ProductWithDescriptor: {product3.price}")
        product3.price = 300
        print(f"Updated Price (descriptor): {product3.price}")
        product3.price = -30
    except ValueError as e:
        print(f"Error in ProductWithDescriptor: {e}")


# Виклик тестових функцій
test_products()
test_products_with_currency()
