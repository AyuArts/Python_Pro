def analyze_object(obj):
    """
    Аналізує об'єкт, виводячи його тип, користувацькі методи та атрибути разом з їхніми типами.

    :param unknown_obj: будь-який об'єкт для аналізу
    """
    # Виводимо тип об'єкта
    print(f"Тип об'єкта: {type(obj)}\n")

    # Отримуємо всі атрибути та методи об'єкта, виключаючи ті, що починаються на '__'
    attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
    print("Атрибути і методи:")

    # Виводимо кожен атрибут та його тип
    for attr in attributes:
        try:
            # Отримуємо значення атрибута
            value = getattr(obj, attr)
            # Виводимо атрибут та його тип
            print(f"- {attr}: {type(value)}")
        except AttributeError:
            print(f"- {attr}: не вдається отримати значення")


# Приклад використання
class MyClass:
    def __init__(self, value):
        self.value = value

    def say_hello(self):
        return f"Hello, {self.value}"

obj = MyClass("World")
analyze_object(obj)