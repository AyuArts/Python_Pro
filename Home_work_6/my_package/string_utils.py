def upper_case(str: str) -> str:
    """
    Перетворює всі символи рядка на великі літери.

    :param str: Вхідний рядок, який потрібно перетворити.
    :return: Рядок з усіма символами у верхньому регістрі.
    """
    return str.upper()


def lower_case(str: str) -> str:
    """
    Перетворює всі символи рядка на малі літери.

    :param str: Вхідний рядок, який потрібно перетворити.
    :return: Рядок з усіма символами у нижньому регістрі.
    """
    return str.lower()


def removing_spaces(str: str) -> str:
    """
    Видаляє пробіли на початку та в кінці рядка.

    :param str: Вхідний рядок, з якого потрібно видалити пробіли.
    :return: Рядок без пробілів на початку та в кінці.
    """
    return str.strip()
