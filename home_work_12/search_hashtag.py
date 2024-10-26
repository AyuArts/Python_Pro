import re


def search_hashtag(text):
    """
    Пошук усіх хештегів у тексті та їх передача для перевірки унікальності.

    :param text: Вхідний текст, у якому здійснюється пошук хештегів.
    :type text: str
    """
    hashtags = re.findall(r"(\#\w+\_?\w+)", text)
    validata_unique_hashtag(hashtags)


def validata_unique_hashtag(hashtags):
    """
    Перевірка та виведення унікальних хештегів зі списку.

    :param hashtags: Список знайдених хештегів.
    :type hashtags: list
    """
    unique_hashtag = set()
    for hashtag in hashtags:
        if hashtag not in unique_hashtag:
            unique_hashtag.add(hashtag)
            print(f"Хештег: {hashtag}")


text = """
Today we are launching our new project! #New_Project #Growth #Technology #Innovation #DreamTeam

We are excited to share the first results of our work! Thank you all for your support #Success #Support #Motivation #StepToGoal

Stay tuned for updates, there’s more to come! #Updates #Ideas #Inspiration #Changes #Progress

Join our team and reach new heights with us! #Career #NewJob #Opportunity #DreamsComeTrue

Don't forget to stay with us for the latest news! #News #Events #Future #StayTuned
"""

search_hashtag(text)
