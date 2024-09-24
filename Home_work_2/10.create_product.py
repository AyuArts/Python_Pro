# Task 10

def create_product(name, price, quantity):
    """
    Створює продукт із заданими параметрами та повертає функції для отримання інформації і оновлення ціни.

    Аргументи:
    name (str): Назва продукту.
    price (float): Ціна продукту.
    quantity (int): Кількість продукту на складі.

    Повертає:
    tuple: Функції get_info та set_price для управління продуктом.
    """
    product = {
        "name": name,
        "price": price,
        "quantity": quantity
    }

    def get_info():
        """
        Повертає інформацію про продукт у вигляді рядка.

        Повертає:
        str: Опис продукту з назвою, ціною і кількістю.
        """
        return f"Продукт: {product['name']}, Ціна: {product['price']}, Кількість: {product['quantity']}"

    def set_price(new_price):
        """
        Оновлює ціну продукту.

        Аргументи:
        new_price (float): Нова ціна продукту.

        Повертає:
        str: Повідомлення про успішне оновлення ціни.
        """
        product['price'] = new_price
        return f"Ціна за {product['name']} була оновлена до {product['price']}."

    return get_info, set_price


# Створюємо продукт і отримуємо функції для роботи з ним
get_info, set_price = create_product("Laptop", 1000, 10)

# Отримуємо інформацію про продукт
print(get_info())

# Оновлюємо ціну продукту
print(set_price(1200))

# Перевіряємо оновлену інформацію про продукт
print(get_info())
