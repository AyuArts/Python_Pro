import re


def validata_password(password):
    """
    Перевірка пароля на відповідність вимогам безпеки.

    :param password: Введений пароль.
    :type password: str
    :return: Список повідомлень про помилки, якщо вони є, або порожній список, якщо пароль правильний.
    :rtype: list
    """
    checks = [
        (len(password) < 8, "Пароль повинен містити не менше 8 символів."),
        (not re.search(r"[A-Z]", password), "Пароль повинен містити хоча б одну велику літеру."),
        (not re.search(r"[0-9]", password), "Пароль повинен містити хоча б одну цифру."),
        (not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Пароль повинен містити хоча б один спеціальний символ.")
    ]

    return [message for condition, message in checks if condition]


def input_to_password():
    """
    Функція для введення пароля та перевірки його валідності.

    :return: Повідомлення про валідність або список помилок.
    :rtype: str або list
    """
    password = input("Введіть новий пароль: ")
    valid = validata_password(password)
    if not valid:
        return "Вірний пароль"
    else:
        return valid


print(input_to_password())
