# Task 3 ==============================================

def create_order(value, add_discount):
    discounted_price = value - (value * discount)
    new_product_price = discounted_price

    def apply_additional_discount():
        nonlocal new_product_price, discounted_price

        if add_discount == "vip":
            additional_discount = 0.3
        else:
            additional_discount = 0

        new_product_price = discounted_price - (discounted_price * additional_discount)

    apply_additional_discount()

    def correct_price():
        nonlocal new_product_price

        price_check = new_product_price - int(new_product_price)

        if price_check == 0.0:
            new_product_price = int(new_product_price)
        else:
            new_product_price = "{:.2f}".format(new_product_price)

    correct_price()

    print(f"Кінцева ціна товару: {new_product_price} гривен")


discount = 0.1
create_order(1000, "vip")
