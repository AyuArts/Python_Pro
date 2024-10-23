"""
Цей модуль реалізує взаємодію з базою даних MongoDB для продуктів і замовлень
у продуктовому магазині.

Використовуються моделі для валідації даних продуктів і замовлень за допомогою Pydantic.
Модуль включає методи для створення колекцій, вставки продуктів і замовлень, а також
для обробки замовлень і перегляду недавніх операцій.
"""
from pydantic import BaseModel, ValidationError, PositiveInt, PositiveFloat
from typing import List, Tuple
from enum import Enum
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from logs.log_config import get_custom_logger  # Імпортуємо фабричну функцію для отримання логера
from datetime import datetime, timedelta


class Collections(Enum):
    """
    Перелік можливих колекцій у базі даних MongoDB.
    """
    PRODUCTS = "products"
    ORDERS = "orders"


class ProductModel(BaseModel):
    """
    Модель для валідації продуктів.

    :param product_name (str): Назва продукту.
    :param quantity (PositiveInt): Кількість продукту (позитивне ціле число).
    :param category (str): Категорія продукту.
    :param price (PositiveFloat): Ціна продукту (позитивне число).
    """
    product_name: str
    quantity: PositiveInt
    category: str
    price: PositiveFloat


class OrderItem(BaseModel):
    """
    Модель для валідації одиниць замовлення.

    :param product_name (str): Назва продукту в замовленні.
    :param quantity (PositiveInt): Кількість одиниць продукту.
    """
    product_name: str
    quantity: PositiveInt


class OrderModel(BaseModel):
    """
    Модель для валідації замовлень.

    Атрибути:
        client_name (str): Ім'я клієнта, що робить замовлення.
        products_list (List[OrderItem]): Список замовлених продуктів.
    """
    client_name: str
    products_list: List[OrderItem]


class MyMongo:
    """
    Клас для роботи з базою даних MongoDB.

    Метод забезпечує керування підключенням до бази, створення колекцій, додавання продуктів,
    оформлення замовлень, а також перегляд інформації про продажі.

    Атрибути:
        host (str): Адреса хоста MongoDB.
        port (int): Порт для підключення до MongoDB.
        database_name (str): Назва бази даних MongoDB.
        client: Об'єкт MongoClient для взаємодії з базою даних.
        db: Поточна база даних, з якою працює клас.
        logger: Логгер для ведення журналу подій.
    """

    def __init__(self, host: str, port: int, database: str):
        """
        Ініціалізує підключення до бази даних MongoDB.

        Аргументи:
            host (str): Адреса хоста MongoDB.
            port (int): Порт для підключення до MongoDB.
            database (str): Назва бази даних.
        """
        self.host = host
        self.port = port
        self.database_name = database
        self.client = None
        self.db = None
        self.message = "messages_mongo.json"  # Назва файлу без шляху

        # Ініціалізація логера з файлом повідомлень
        self.logger = get_custom_logger(self.message)

    def __enter__(self):
        """
        Встановлює підключення до MongoDB при вході в контекстний менеджер.

        Повертає:
            MyMongoDB: Об'єкт для подальшої роботи з базою даних.
        """
        try:
            self.client = MongoClient(self.host, self.port, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database_name]
            # Перевірка підключення
            self.client.admin.command('ping')
            self.logger.info(['database', 'connected'], db_name=self.db.name)
            return self
        except ConnectionFailure as e:
            self.logger.error(['database', 'connection_error'], error=str(e))
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закриває підключення до MongoDB при виході з контекстного менеджера.
        """
        if self.client:
            self.client.close()
            self.logger.info(['database', 'connection_closed'])
        if exc_type:
            self.logger.error(['general', 'exception_in_with_block'], error=str(exc_value))
        return False

    def create_collections(self):
        """
        Створює колекції в базі даних: продукти і замовлення.
        """
        self.setup_products_collection()
        self.setup_orders_collection()

    def setup_products_collection(self):
        """
        Налаштовує колекцію 'products' у базі даних.

        Створює необхідні індекси для колекції продуктів:
        - Індекс для поля 'category' (неунікальний).
        - Індекс для поля 'product_name' (унікальний).

        Видаляє унікальний індекс для поля 'category', якщо він існує.
        """
        products_collection = self.db[Collections.PRODUCTS.value]
        self.remove_unique_index(products_collection, 'category')
        self.create_index(
            products_collection,
            [('category', ASCENDING)],
            unique=False,
            message_keys=['collections', 'index_created'],
            field='category',
            collection_name='products'
        )
        self.create_index(
            products_collection,
            [('product_name', ASCENDING)],
            unique=True,
            message_keys=['collections', 'index_created'],
            field='product_name',
            collection_name='products'
        )

    def setup_orders_collection(self):
        """
        Налаштовує колекцію 'orders' у базі даних.

        Створює необхідні індекси для колекції замовлень:
        - Індекс для поля 'order_number' (унікальний).
        - Індекс для поля 'order_date' (неунікальний).
        """
        orders_collection = self.db[Collections.ORDERS.value]
        self.create_index(
            orders_collection,
            [('order_number', ASCENDING)],
            unique=True,
            message_keys=['collections', 'index_created'],
            field='order_number',
            collection_name='orders'
        )
        self.create_index(
            orders_collection,
            [('order_date', ASCENDING)],
            unique=False,
            message_keys=['collections', 'index_created'],
            field='order_date',
            collection_name='orders'
        )

    def remove_unique_index(self, collection, field_name: str):
        """
        Видаляє унікальний індекс для вказаного поля, якщо такий існує.

        Аргументи:
            collection: Колекція, в якій необхідно видалити індекс.
            field_name (str): Поле, індекс якого необхідно видалити.
        """
        indexes = collection.index_information()
        index_name = f"{field_name}_1"
        if index_name in indexes and indexes[index_name].get('unique'):
            collection.drop_index(index_name)
            self.logger.info(['collections', 'index_dropped'], field=field_name, collection_name=collection.name)

    def create_index(self, collection, keys, unique=False, message_keys=None, **kwargs):
        """
        Створює індекс для колекції MongoDB.

        Аргументи:
            collection: Колекція, для якої створюється індекс.
            keys: Поля, за якими створюється індекс.
            unique (bool): Чи є індекс унікальним.
            message_keys: Ключі для локалізованого повідомлення про створення індексу.
            **kwargs: Додаткові параметри для логування.
        """
        collection.create_index(keys, unique=unique)
        if message_keys:
            self.logger.info(message_keys, **kwargs)

    def insert_product(self, product_name: str, quantity: int, category: str, price: float):
        """
        Вставляє або оновлює продукт у колекції 'products'.

        Аргументи:
            product_name (str): Назва продукту.
            quantity (int): Кількість продукту.
            category (str): Категорія продукту.
            price (float): Ціна продукту.
        """
        product = self.validate_product_data(product_name, quantity, category, price)
        if not product:
            return
        collection = self.db[Collections.PRODUCTS.value]
        self.upsert_product(collection, product)

    def validate_product_data(self, product_name: str, quantity: int, category: str, price: float):
        """
        Валідує дані продукту перед вставкою.

        Аргументи:
            product_name (str): Назва продукту.
            quantity (int): Кількість продукту.
            category (str): Категорія продукту.
            price (float): Ціна продукту.

        Повертає:
            ProductModel або None: Валідована модель продукту або None у разі помилки валідації.
        """
        try:
            product = ProductModel(
                product_name=product_name,
                quantity=quantity,
                category=category,
                price=price
            )
            return product
        except ValidationError as e:
            self.logger.error(['validation', 'product_validation_error'], error=str(e))
            return None

    def upsert_product(self, collection, product: ProductModel):
        """
        Вставляє або оновлює інформацію про продукт у колекції.

        Аргументи:
            collection: Колекція продуктів.
            product (ProductModel): Валідована модель продукту.
        """
        result = collection.update_one(
            {"product_name": product.product_name},
            {"$inc": {"quantity": product.quantity}, "$set": {"price": product.price, "category": product.category}},
            upsert=True
        )
        if result.upserted_id:
            self.logger.info(['products', 'product_added'], product_name=product.product_name,
                             category=product.category)
        elif result.modified_count:
            self.logger.info(['products', 'product_updated'], product_name=product.product_name)
        else:
            self.logger.error(['products', 'product_upsert_error'], product_name=product.product_name)

    def find_product_by_name(self, product_name: str):
        """
        Знаходить продукт у колекції 'products' за назвою.

        Аргументи:
            product_name (str): Назва продукту.

        Повертає:
            dict або None: Інформація про продукт або None, якщо продукт не знайдено.
        """
        return self.db[Collections.PRODUCTS.value].find_one({"product_name": product_name})

    def insert_order(self, client_name: str, *products):
        """
        Вставляє нове замовлення в колекцію 'orders'.

        Аргументи:
            client_name (str): Ім'я клієнта.
            *products: Продукти та їх кількість у вигляді кортежів (назва продукту, кількість).
        """
        products_list = self.prepare_products_list(*products)
        if not products_list:
            self.logger.error(['orders', 'empty_or_invalid_product_list'])
            return
        order_data = self.validate_order_data(client_name, products_list)
        if not order_data:
            return
        orders_collection = self.db[Collections.ORDERS.value]
        products_collection = self.db[Collections.PRODUCTS.value]
        order_number = self.generate_order_number(orders_collection)
        products_to_update, total_sum, messages = self.process_order_items(order_data, products_collection)
        if not products_to_update:
            self.logger.info(['orders', 'order_not_created'])
            return
        self.update_product_quantities(products_collection, products_to_update)
        self.remove_zero_quantity_products(products_collection)
        self.insert_order_document(orders_collection, order_data, order_number, total_sum, messages)
        self.log_messages(messages)

    def prepare_products_list(self, *products) -> List[OrderItem]:
        """
        Готує список замовлених продуктів для валідації.

        Аргументи:
            *products: Продукти у вигляді кортежів (назва продукту, кількість).

        Повертає:
            List[OrderItem] або порожній список: Валідований список продуктів або порожній список у разі помилок валідації.
        """
        products_list = []
        for item in products:
            if isinstance(item, (tuple, list)) and len(item) == 2:
                product_name, quantity = item
                try:
                    order_item = OrderItem(product_name=product_name, quantity=quantity)
                    products_list.append(order_item)
                except ValidationError as e:
                    self.logger.error(['validation', 'order_item_validation_error'], error=str(e))
                    return []
            else:
                self.logger.error(['validation', 'invalid_product_format'], item=str(item))
                return []
        return products_list

    def validate_order_data(self, client_name: str, products_list: List[OrderItem]):
        """
        Валідує дані замовлення.

        Аргументи:
            client_name (str): Ім'я клієнта.
            products_list (List[OrderItem]): Список продуктів у замовленні.

        Повертає:
            OrderModel або None: Валідована модель замовлення або None у разі помилки валідації.
        """
        try:
            order_data = OrderModel(
                client_name=client_name,
                products_list=products_list
            )
            return order_data
        except ValidationError as e:
            self.logger.error(['validation', 'order_validation_error'], error=str(e))
            return None

    @staticmethod
    def generate_order_number(orders_collection) -> int:
        """
        Генерує новий номер замовлення на основі попереднього замовлення.

        Аргументи:
            orders_collection: Колекція замовлень.

        Повертає:
            int: Наступний номер замовлення.
        """
        last_order = orders_collection.find_one(
            sort=[("order_number", -1)])
        if last_order and "order_number" in last_order:
            return last_order["order_number"] + 1
        else:
            return 1

    def process_order_items(self, order_data: OrderModel, products_collection):
        """
        Обробляє замовлені товари, перевіряючи їх наявність і оновлюючи кількість товарів.

        Аргументи:
            order_data (OrderModel): Дані замовлення, що містять список продуктів.
            products_collection: Колекція продуктів у базі даних.

        Повертає:
            Tuple[List[Tuple[str, int]], float, List[str]]: Список продуктів для оновлення, загальна сума замовлення та повідомлення.
        """
        total_sum = 0.0
        products_to_update = []
        messages = []

        for item in order_data.products_list:
            product_name = item.product_name
            quantity = item.quantity
            product = products_collection.find_one({"product_name": product_name})
            message, available_quantity = self.check_product_availability(product, product_name, quantity)
            if message:
                messages.append(message)
                if available_quantity == 0:
                    continue
                else:
                    item.quantity = available_quantity
            if product:
                total_sum += product["price"] * item.quantity
                products_to_update.append((product_name, item.quantity))
            else:
                # Продукт не знайдено, вже було залоговано у check_product_availability
                continue

        return products_to_update, total_sum, messages

    def check_product_availability(self, product: dict, product_name: str, requested_quantity: int):
        """
        Перевіряє наявність товару на складі та повертає відповідне повідомлення.

        Аргументи:
            product (dict): Дані продукту з бази.
            product_name (str): Назва продукту.
            requested_quantity (int): Кількість продукту, яку запитує клієнт.

        Повертає:
            Tuple[str, int]: Повідомлення про наявність та кількість доступного продукту.
        """
        if not product:
            self.logger.info(['availability', 'product_not_available'], product_name=product_name)
            return "Продукт не доступний.", 0
        if product["quantity"] == 0:
            self.logger.info(['availability', 'product_finished'], product_name=product_name)
            return "Продукт закінчився.", 0
        if product["quantity"] < requested_quantity:
            self.logger.info(['availability', 'product_limited_quantity'], product_name=product_name,
                             available_quantity=product["quantity"])
            return f"Продукту {product_name} залишилося лише {product['quantity']}.", product["quantity"]
        else:
            if product["quantity"] == requested_quantity:
                self.logger.info(['availability', 'product_fully_purchased'], product_name=product_name)
            return "", requested_quantity

    def update_product_quantities(self, products_collection, products_to_update):
        """
        Оновлює кількість продуктів у колекції на основі замовлення.

        Аргументи:
            products_collection: Колекція продуктів.
            products_to_update (List[Tuple[str, int]]): Список продуктів з їх кількістю для оновлення.
        """
        for product_name, quantity in products_to_update:
            result = products_collection.update_one(
                {"product_name": product_name},
                {"$inc": {"quantity": -quantity}}
            )
            if result.modified_count:
                self.logger.info(['products', 'product_quantity_updated'], product_name=product_name)
            else:
                self.logger.error(['products', 'product_quantity_update_error'], product_name=product_name)

    def remove_zero_quantity_products(self, products_collection):
        """
        Видаляє продукти, кількість яких дорівнює або менше 0 з колекції 'products'.

        Аргументи:
            products_collection: Колекція продуктів.
        """
        delete_result = products_collection.delete_many({"quantity": {"$lte": 0}})
        if delete_result.deleted_count:
            self.logger.info(['products', 'product_removed'], count=delete_result.deleted_count)

    def insert_order_document(self, orders_collection, order_data: OrderModel, order_number: int, total_sum: float,
                              messages: List[str]):
        """
        Вставляє документ замовлення в колекцію 'orders'.

        Аргументи:
            orders_collection: Колекція замовлень.
            order_data (OrderModel): Дані замовлення, що включають інформацію про клієнта та продукти.
            order_number (int): Номер замовлення.
            total_sum (float): Загальна сума замовлення.
            messages (List[str]): Список повідомлень, пов'язаних із замовленням.
        """
        new_order = {
            "order_number": order_number,
            "client_name": order_data.client_name,
            "products_list": [item.model_dump() for item in order_data.products_list],
            "total_sum": total_sum,
            "messages": messages,
            "order_date": datetime.now()
        }
        orders_collection.insert_one(new_order)
        self.logger.info(['orders', 'order_created'], order_number=order_number, client_name=order_data.client_name)

    def log_messages(self, messages: List[str]):
        """
        Логує повідомлення, пов'язані з замовленням.

        Аргументи:
            messages (List[str]): Список повідомлень для логування.
        """
        for message in messages:
            self.logger.info(['orders', 'message'], message=message)

    def show_recent_orders(self, days: int = 30):
        """
        Показує замовлення, зроблені за останні N днів.

        Аргументи:
            days (int): Кількість днів для фільтрації замовлень (за замовчуванням 30).
        """
        date_threshold = datetime.now() - timedelta(days=days)
        orders_collection = self.db[Collections.ORDERS.value]
        recent_orders = list(orders_collection.find({"order_date": {"$gte": date_threshold}}))
        count = len(recent_orders)
        self.logger.info(['orders', 'recent_orders_retrieved'], count=count, days=days)
        self.logger.info(['orders', 'recent_orders_count'], count=count, days=days)

    def show_total_products_sold(self, days: int = 30):
        """
        Показує загальну кількість проданих продуктів за останні N днів.

        Аргументи:
            days (int): Кількість днів для підрахунку проданих продуктів (за замовчуванням 30).
        """
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()
        orders_collection = self.db[Collections.ORDERS.value]
        pipeline = [
            {"$match": {"order_date": {"$gte": start_date, "$lte": end_date}}},
            {"$unwind": "$products_list"},
            {"$group": {
                "_id": "$products_list.product_name",
                "total_sold": {"$sum": "$products_list.quantity"}
            }}
        ]
        total_products_sold = list(orders_collection.aggregate(pipeline))
        self.logger.info(['orders', 'total_products_sold_retrieved'], start_date=start_date, end_date=end_date)
        # Логуємо інформацію про продані продукти
        for product in total_products_sold:
            self.logger.info(['orders', 'product_sold'], product_name=product['_id'], total_sold=product['total_sold'])

    def insert_products(self, products: List[Tuple[str, int, str, float]]):
        """
        Вставляє кілька продуктів у колекцію 'products'.

        Аргументи:
            products (List[Tuple[str, int, str, float]]): Список кортежів з даними продукту (назва, кількість, категорія, ціна).
        """
        validated_products = []
        for product_data in products:
            product = self.validate_product_data(*product_data)
            if product:
                validated_products.append(product)
        if not validated_products:
            self.logger.error(['products', 'product_not_validated'])
            return
        collection = self.db[Collections.PRODUCTS.value]
        for product in validated_products:
            self.upsert_product(collection, product)

    def show_total_spent_by_client(self, client_name: str):
        """
        Показує загальну суму, витрачену клієнтом.

        Аргументи:
            client_name (str): Ім'я клієнта, для якого потрібно підрахувати витрати.
        """
        orders_collection = self.db[Collections.ORDERS.value]
        pipeline = [
            {"$match": {"client_name": client_name}},
            {"$group": {
                "_id": "$client_name",
                "total_spent": {"$sum": "$total_sum"}
            }}
        ]
        result = list(orders_collection.aggregate(pipeline))
        if result:
            total_spent = result[0]['total_spent']
            self.logger.info(['orders', 'total_spent_retrieved'], client_name=client_name, total_spent=total_spent)
        else:
            self.logger.info(['orders', 'no_orders_for_client'], client_name=client_name)


# Приклад Використання
if __name__ == "__main__":
    with MyMongo("localhost", 27017, "grocery_store") as gs:
        gs.create_collections()

        gs.insert_products([
            ("Apple", 100, "fruit", 1.25),
            ("Banana", 150, "fruit", 0.99),
            ("Carrot", 50, "vegetable", 0.50),
            ("Orange", 80, "fruit", 1.10),
            ("Potato", 200, "vegetable", 0.30)
        ])
        # Вставка продуктів
        gs.insert_product("Apple", 100, "fruit", 1.25)
        gs.insert_product("Banana", 150, "fruit", 0.99)
        gs.insert_product("Carrot", 50, "vegetable", 0.50)
        gs.insert_product("Orange", 80, "fruit", 1.10)
        gs.insert_product("Potato", 200, "vegetable", 0.30)

        # Вставка замовлень
        gs.insert_order("John Doe", ("Apple", 50), ("Banana", 30))
        gs.insert_order("Jane Smith", ("Banana", 50), ("Carrot", 20))
        gs.insert_order("Bob Brown", ("Carrot", 20), ("Potato", 100))
        gs.insert_order("Alice Johnson", ("Orange", 40), ("Apple", 30))

        gs.show_recent_orders(30)
        gs.show_total_products_sold(30)
        gs.show_total_spent_by_client("John Doe")
