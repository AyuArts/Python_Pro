import re

class User:
    """
    Клас User для управління даними користувача.

    Атрибути:
    ----------
    __first_name : str
        Ім'я користувача.
    __last_name : str
        Прізвище користувача.
    __email : str
        Email користувача.
    __password : str
        Пароль користувача.
    """

    def __init__(self):
        """
        Ініціалізує екземпляр класу User з початковими значеннями.
        """
        self.__first_name = None
        self.__last_name = None
        self.__email = None
        self.__password = None

    def validate_field(self, field_type, value, value_check=None):
        """
        Валідує різні типи полів.

        :param field_type: Тип поля, яке потрібно перевірити (наприклад, 'first_name', 'password').
        :param value: Значення, яке необхідно перевірити.
        :param value_check: Додаткове значення для порівняння (наприклад, при підтвердженні пароля або email), опціонально.
        :return: Список повідомлень про помилки, якщо такі є.
        """
        checks = []

        if field_type == "password":
            checks = [
                (len(value) < 8, "The password must contain at least 8 characters."),
                (not re.search(r"[A-Z]", value), "The password must contain at least one capital letter."),
                (not re.search(r"[0-9]", value), "The password must contain at least one number."),
                (not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value), "The password must contain at least one special character.")
            ]

        elif field_type == "password_confirmation":
            checks = [
                (value != value_check, "The passwords do not match."),
            ]

        elif field_type == "email":
            checks = [
                (not re.match(r"^[\w\.-]+@", value), "Email must contain a valid prefix before '@'."),
                (not re.search(r"@[\w\.-]+", value), "Email must contain a valid domain after '@'."),
                (not re.search(r"\.[a-zA-Z]{2,}$", value),
                 "Email must contain a valid domain extension (e.g., '.com', '.org')."),
                (re.search(r"[!#\$%^&*(),?\":{}|<> ]", value), "Email contains invalid characters.")
            ]

        elif field_type in ["first_name", "last_name"]:
            if re.search(r"[А-Яа-я]", value):
                checks.append((True, f"{field_type.capitalize().replace('_', ' ')} can only contain Latin letters, apostrophes, or hyphens."))
            else:
                checks.append((len(value) < 2, f"{field_type.capitalize().replace('_', ' ')} must be at least 2 characters long."))
                checks.append((not re.match(r"^[A-Za-z'-]+$", value), f"{field_type.capitalize().replace('_', ' ')} can only contain Latin letters, apostrophes, or hyphens."))

        return [message for condition, message in checks if condition]

    @property
    def first_name(self):
        """
        Повертає ім'я користувача.

        :return: Ім'я користувача (str).
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """
        Встановлює значення first_name після валідації.

        :param value: Ім'я користувача (str).
        :raises ValueError: Якщо валідація не пройдена.
        """
        errors = self.validate_field("first_name", value)
        if errors:
            raise ValueError(errors[0])
        self.__first_name = value

    @property
    def last_name(self):
        """
        Повертає прізвище користувача.

        :return: Прізвище користувача (str).
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """
        Встановлює значення last_name після валідації.

        :param value: Прізвище користувача (str).
        :raises ValueError: Якщо валідація не пройдена.
        """
        errors = self.validate_field("last_name", value)
        if errors:
            raise ValueError(errors[0])
        self.__last_name = value

    @property
    def email(self):
        """
        Повертає email користувача.

        :return: Email користувача (str).
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Встановлює значення email після валідації.

        :param value: Email користувача (str).
        :raises ValueError: Якщо валідація не пройдена.
        """
        errors = self.validate_field("email", value)
        if errors:
            raise ValueError(errors[0])
        self.__email = value

    @property
    def password(self):
        """
        Повертає пароль користувача.

        :return: Пароль користувача (str).
        """
        return self.__password

    @password.setter
    def password(self, value):
        """
        Встановлює значення password після валідації.

        :param value: Пароль користувача (str).
        :raises ValueError: Якщо валідація не пройдена.
        """
        errors = self.validate_field("password", value)
        if errors:
            raise ValueError(errors[0])
        self.__password = value

    def get_valid_input(self, field_type, prompt, value_check=None):
        """
        Отримує коректний ввід з повторними спробами.

        :param field_type: Тип поля, яке потрібно перевірити (str).
        :param prompt: Повідомлення для введення (str).
        :param value_check: Додаткове значення для перевірки (str), опціонально.
        :return: Коректне значення (str).
        """
        attempts = 0
        while attempts < 3:
            value = input(prompt)
            errors = self.validate_field(field_type, value, value_check)
            if not errors:
                return value
            else:
                for error in errors:
                    print(f"Error: {error}")
                attempts += 1
                print(f"Attempt {attempts} of 3 failed.")

        print(f"Too many failed attempts for {field_type}. Exiting...")
        exit(1)

    def collect_user_data(self):
        """
        Збирає дані користувача з перевіркою кожного поля.
        """
        self.first_name = self.get_valid_input("first_name", "Enter your first name: ")
        self.last_name = self.get_valid_input("last_name", "Enter your last name: ")

        password = self.get_valid_input("password", "Enter your password: ")
        self.get_valid_input("password_confirmation", "Enter your password again: ", value_check=password)
        self.password = password

        email = self.get_valid_input("email", "Enter your email: ")
        self.get_valid_input("email", "Enter your email again: ", value_check=email)
        self.email = email

    def get_user_data(self):
        """
        Повертає дані користувача.

        :return: Словник з даними користувача (dict).
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }


def test_user_class():
    """
    Розширене тестування класу User з різними вхідними даними.
    """
    # Тест 1: Коректні дані
    print("Тест 1: Коректні дані")
    try:
        user = User()
        user.first_name = "John"
        user.last_name = "Doe"
        user.password = "Password123!"
        user.email = "john.doe@example.com"
        print("Дані користувача:", user.get_user_data())
        print("Тест 1 пройдено.")
    except ValueError as e:
        print(f"Тест 1 не пройдено: {e}")

    # Тест 2: Занадто коротке ім'я
    print("\nТест 2: Занадто коротке ім'я")
    try:
        user = User()
        user.first_name = "J"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 2 пройдено.")

    # Тест 3: Використання кирилиці у полі імені
    print("\nТест 3: Використання кирилиці у полі імені")
    try:
        user = User()
        user.first_name = "Іван"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 3 пройдено.")

    # Тест 4: Некоректний формат email
    print("\nТест 4: Некоректний формат email")
    try:
        user = User()
        user.email = "invalid-email"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 4 пройдено.")

    # Тест 5: Невідповідність паролів
    print("\nТест 5: Невідповідність паролів")
    try:
        user = User()
        user.password = "Password123!"
        user.get_valid_input("password_check", "Повторіть пароль: ", value_check="Password123")
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 5 пройдено.")

    # Тест 6: Пароль без великої літери
    print("\nТест 6: Пароль без великої літери")
    try:
        user = User()
        user.password = "password123!"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 6 пройдено.")

    # Тест 7: Пароль без цифри
    print("\nТест 7: Пароль без цифри")
    try:
        user = User()
        user.password = "Password!"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 7 пройдено.")

    # Тест 8: Пароль без спеціального символу
    print("\nТест 8: Пароль без спеціального символу")
    try:
        user = User()
        user.password = "Password123"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 8 пройдено.")

    # Тест 9: Некоректний email без домену
    print("\nТест 9: Некоректний email без домену")
    try:
        user = User()
        user.email = "john.doe@"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 9 пройдено.")

    # Тест 10: Некоректний email без префікса
    print("\nТест 10: Некоректний email без префікса")
    try:
        user = User()
        user.email = "@example.com"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 10 пройдено.")

    # Тест 11: Некоректний email без крапки у домені
    print("\nТест 11: Некоректний email без крапки у домені")
    try:
        user = User()
        user.email = "john.doe@examplecom"
    except ValueError as e:
        print(f"Очікувана помилка: {e}")
        print("Тест 11 пройдено.")

    # Тест 12: Дуже довге ім'я
    print("\nТест 12: Дуже довге ім'я")
    try:
        user = User()
        user.first_name = "A" * 256  # 256 символів
        print(f"Довжина імені: {len(user.first_name)}")
        print("Тест 12 пройдено.")
    except ValueError as e:
        print(f"Тест 12 не пройдено: {e}")

    # Тест 13: Повне введення користувача
    print("\nТест 13: Повне введення користувача")
    try:
        user = User()
        user.first_name = "Alice"
        user.last_name = "Smith"
        user.password = "StrongPassword1!"
        user.email = "alice.smith@example.com"
        print("Дані користувача:", user.get_user_data())
        print("Тест 13 пройдено.")
    except ValueError as e:
        print(f"Тест 13 не пройдено: {e}")


# Виклик тестів
test_user_class()
