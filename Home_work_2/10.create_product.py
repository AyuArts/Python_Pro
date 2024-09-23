# Task 10 ==============================================

def create_product(name, price, quantity):

    product = {
        "name": name,
        "price": price,
        "quantity": quantity
    }


    def get_info():
        return f"Продукт: {product['name']}, Ціна: {product['price']}, Кількість: {product['quantity']}"


    def set_price(new_price):
        product['price'] = new_price
        return f"Ціна за {product['name']} була оновленa до {product['price']}."


    return get_info, set_price



get_info, set_price = create_product("Laptop", 1000, 10)


print(get_info())


print(set_price(1200))


print(get_info())