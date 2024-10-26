import re


def create_new_date(date):
    """
    Форматує дату з формату дд/мм/рррр у формат рррр-мм-дд.

    :param date: Вхідна дата у форматі дд/мм/рррр.
    :type date: str
    :return: Дата у форматі рррр-мм-дд або повідомлення "invalid date" у разі невідповідності формату.
    :rtype: str
    """
    pattern = r'(\d{,2})\/(\d{,2})\/(\d{4})'
    if re.match(pattern, date):
        new_date = re.sub(pattern, r"\3-\2-\1", date)
        return new_date
    else:
        return "invalid date"


print(create_new_date('1/03/1995'))
