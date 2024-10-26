import re


def validata_email(email):
    """
    Перевірка електронної пошти на відповідність вимогам формату.

    :param email: Введена електронна пошта.
    :type email: str
    :return: Список повідомлень про помилки, якщо вони є, або порожній список, якщо формат правильний.
    :rtype: list
    """
    checks = [
        (not re.match(r"^[\w\.-]+@", email),
         "Електронна пошта повинна містити дійсний префікс до '@'."),
        (not re.search(r"@[\w\.-]+", email),
         "Електронна пошта повинна містити дійсний домен після '@'."),
        (not re.search(r"\.[a-zA-Z]{2,}$", email),
         "Електронна пошта повинна містити дійсне розширення домену (наприклад, '.com', '.org')."),
        (re.search(r"[!#\$%^&*(),?\":{}|<> ]", email),
         "Електронна пошта містить неприпустимі символи.")
    ]

    return [message for condition, message in checks if condition]


def input_to_email():
    """
    Функція для введення електронної пошти та перевірки її валідності.

    :return: Повідомлення про валідність або список помилок.
    :rtype: str або list
    """
    email = input("Введіть свою електронну пошту: ")
    valid = validata_email(email)
    if not valid:
        return "Вірна електронна пошта"
    else:
        return valid


print(input_to_email())
