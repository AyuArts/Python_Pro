def create_class(class_name, methods, doc=None):
    """
    Створює динамічний клас з вказаною назвою, методами та документацією.

    :param class_name: Назва динамічно створюваного класу.
    :param methods: Словник, що містить методи класу у форматі {ім'я_методу: функція}.
    :param doc: Документація для класу (рядок). За замовчуванням None.
    :return: Динамічно створений клас.
    """
    # Додаємо документацію до класу, якщо вона передана
    if doc:
        methods['__doc__'] = doc
    return type(class_name, (), methods)

# Методи для класу
def say_hello(self):
    """Повертає привітання."""
    return "Hello!"

def say_goodbye(self):
    """Повертає прощання."""
    return "Goodbye!"

# Словник методів
methods = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye
}

# Створюємо клас з документацією
MyDynamicClass = create_class("MyDynamicClass", methods, "Це динамічно створений клас, що містить методи привітання та прощання.")

# Створюємо об'єкт класу і викликаємо методи
obj = MyDynamicClass()
print(obj.say_hello())  # Виведе: Hello!
print(obj.say_goodbye())  # Виведе: Goodbye!

# Виведення документації
print(MyDynamicClass.__doc__)  # Документація класу
print(MyDynamicClass.say_hello.__doc__)  # Документація методу say_hello
print(MyDynamicClass.say_goodbye.__doc__)  # Документація методу say_goodbye
