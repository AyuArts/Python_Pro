from lxml import etree

def handle_xml_file(xml_file, data=None, mode='load'):
    """
    Універсальна функція для завантаження або збереження даних з/до XML-файлу.

    :param xml_file: Шлях до XML-файлу.
    :param data: Дані для збереження (необов'язково).
    :param mode: Режим роботи функції ('load' або 'save').
    :return: Кореневий елемент дерева та саме дерево, якщо режим 'load'. Інакше None.
    """
    try:
        if mode == 'load':
            tree = etree.parse(xml_file)
            return tree.getroot(), tree
        elif mode == 'save' and data is not None:
            tree = etree.ElementTree(data)
            tree.write(xml_file, pretty_print=True, encoding='utf-8', xml_declaration=True)
        else:
            raise ValueError("Необхідний список даних для збереження у режимі 'save'.")
    except FileNotFoundError:
        print(f"\nФайл '{xml_file}' не знайдено.")
        return None, None if mode == 'save' else []
    except etree.XMLSyntaxError:
        print(f"\nПомилка під час читання XML-файлу '{xml_file}'.")
        return None, None if mode == 'load' else None


def products_in_stock(xml_file):
    """
    Функція завантажує XML-файл і виводить список продуктів, які є в наявності.

    :param xml_file: Шлях до XML-файлу.
    """
    root, _ = handle_xml_file(xml_file, mode='load')

    if root is None:
        print("Не вдалося завантажити XML-файл.")
        return

    stock = [product for product in root.findall('product') if int(product.find('quantity').text) > 0]

    if not stock:
        print("Продуктів у наявності немає.")
    else:
        for product in stock:
            name = product.find('name').text
            price = product.find('price').text
            quantity = product.find('quantity').text
            print(f"Назва продукту: {name}"
                  f"\nЦіна продукту: {price}"
                  f"\nКількість на складі: {quantity}\n")


def add_product(xml_file):
    """
    Функція додає новий продукт до XML-файлу.

    :param xml_file: Шлях до XML-файлу.
    """
    root, tree = handle_xml_file(xml_file, mode='load')

    if root is None:
        print("Не вдалося завантажити XML-файл.")
        return

    # Введення даних про продукт
    name_product = input("Введіть назву продукту: ")
    price_product = input("Введіть ціну продукту: ")

    # Валідація кількості
    while True:
        try:
            quantity_product = int(input("Введіть кількість продукту на складі: "))
            break
        except ValueError:
            print("Помилка: Введіть коректну кількість числом.")

    # Створюємо новий продукт як словник
    new_product = {
        "name": name_product,
        "price": price_product,
        "quantity": str(quantity_product)
    }

    # Створюємо XML-елемент з словника
    product_element = etree.Element('product')
    for key, value in new_product.items():
        child = etree.SubElement(product_element, key)
        child.text = value

    # Додаємо новий продукт до кореневого елемента
    root.append(product_element)

    # Форматуємо дерево з правильними відступами
    etree.indent(root, space='    ')

    # Перезаписуємо файл з правильним форматуванням
    handle_xml_file(xml_file, data=root, mode='save')

    print("Продукт успішно доданий.")


def update_product(xml_file):
    """
    Функція дозволяє повністю редагувати продукт (назва, ціна, кількість)
    та зберігає зміни в XML-файл.

    :param xml_file: Шлях до XML-файлу.
    """
    root, tree = handle_xml_file(xml_file, mode='load')

    if root is None:
        print("Не вдалося завантажити XML-файл.")
        return

    # Отримуємо список всіх назв продуктів
    product_names = [product.find('name').text for product in root.findall('product')]

    if not product_names:
        print("Список продуктів порожній.")
        return

    # Виводимо список продуктів
    print("Доступні продукти:")
    for index, name in enumerate(product_names, start=1):
        print(f"{index}. {name}")

    # Вибір продукту для редагування
    while True:
        try:
            choice = int(input("Введіть номер продукту, який ви хочете редагувати: "))
            if 1 <= choice <= len(product_names):
                selected_product_name = product_names[choice - 1]
                break
            else:
                print(f"Будь ласка, введіть число від 1 до {len(product_names)}.")
        except ValueError:
            print("Помилка: Введіть коректний номер продукту.")

    # Знаходимо обраний продукт
    for product in root.findall('product'):
        name = product.find('name').text
        if name == selected_product_name:
            # Виводимо поточні дані продукту
            current_name = product.find('name').text
            current_price = product.find('price').text
            current_quantity = product.find('quantity').text

            print(f"\nРедагування продукту '{current_name}':")
            print(f"1. Назва: {current_name}")
            print(f"2. Ціна: {current_price}")
            print(f"3. Кількість: {current_quantity}")

            # Запитуємо нові дані для продукту (можна залишити порожнім для незмінності)
            new_name = input(f"Нова назва (залиште порожнім для '{current_name}'): ") or current_name
            new_price = input(f"Нова ціна (залиште порожнім для '{current_price}'): ") or current_price
            while True:
                try:
                    new_quantity = input(f"Нова кількість (залиште порожнім для '{current_quantity}'): ") or current_quantity
                    new_quantity = int(new_quantity)
                    break
                except ValueError:
                    print("Помилка: Введіть коректну кількість числом.")

            # Оновлюємо дані продукту
            product.find('name').text = new_name
            product.find('price').text = new_price
            product.find('quantity').text = str(new_quantity)
            break

    # Форматуємо дерево з правильними відступами
    etree.indent(root, space='    ')

    # Перезаписуємо файл з змінами
    handle_xml_file(xml_file, data=root, mode='save')

    print(f"Продукт '{new_name}' успішно оновлено.")


def delete_product(xml_file):
    """
    Функція видаляє продукт з XML-файлу.

    :param xml_file: Шлях до XML-файлу.
    """
    root, tree = handle_xml_file(xml_file, mode='load')

    if root is None:
        print("Не вдалося завантажити XML-файл.")
        return

    # Отримуємо список всіх назв продуктів
    product_names = [product.find('name').text for product in root.findall('product')]

    if not product_names:
        print("Список продуктів порожній.")
        return

    # Виводимо список продуктів
    print("Доступні продукти для видалення:")
    for index, name in enumerate(product_names, start=1):
        print(f"{index}. {name}")

    # Вибір продукту для видалення
    while True:
        try:
            choice = int(input("Введіть номер продукту, який ви хочете видалити: "))
            if 1 <= choice <= len(product_names):
                selected_product_name = product_names[choice - 1]
                break
            else:
                print(f"Будь ласка, введіть число від 1 до {len(product_names)}.")
        except ValueError:
            print("Помилка: Введіть коректний номер продукту.")

    # Підтвердження видалення
    confirm = input(f"Ви впевнені, що хочете видалити продукт '{selected_product_name}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Видалення скасовано.")
        return

    # Знаходимо та видаляємо обраний продукт
    for product in root.findall('product'):
        if product.find('name').text == selected_product_name:
            root.remove(product)
            break

    # Форматуємо дерево з правильними відступами
    etree.indent(root, space='    ')

    # Перезаписуємо файл з змінами
    handle_xml_file(xml_file, data=root, mode='save')

    print(f"Продукт '{selected_product_name}' успішно видалений.")


def menu(xml_file):
    """
    Функція виводить меню і обробляє вибір користувача.

    :param xml_file: Шлях до XML-файлу.
    """
    while True:
        print("\nОберіть дію:")
        print("1. Переглянути продукти в наявності")
        print("2. Додати новий продукт")
        print("3. Редагувати продукт")
        print("4. Видалити продукт")
        print("5. Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            products_in_stock(xml_file)
        elif choice == '2':
            add_product(xml_file)
        elif choice == '3':
            update_product(xml_file)
        elif choice == '4':
            delete_product(xml_file)
        elif choice == '5':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    xml_file = "products.xml"
    menu(xml_file)
