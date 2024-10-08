import requests
import json
import os


def fetch_page_content(url):
    """
    Завантажує сторінку за вказаним URL.

    Параметри:
    - url: URL сторінки для завантаження.

    Повертає:
    - Вміст сторінки у вигляді тексту.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевіряємо на наявність помилок
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка завантаження сторінки: {e}")
        return None


def save_to_text_file(content, text_file):
    """
    Зберігає вміст сторінки у текстовий файл.

    Параметри:
    - content: Вміст сторінки.
    - text_file: Ім'я текстового файлу для збереження.
    """
    try:
        with open(text_file, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Сторінка успішно збережена у текстовий файл: {text_file}")
    except IOError as e:
        print(f"Помилка збереження у текстовий файл: {e}")


def save_to_json_file(content, json_file):
    """
    Зберігає вміст сторінки у файл JSON.

    Параметри:
    - content: Вміст сторінки.
    - json_file: Ім'я JSON файлу для збереження.
    """
    try:
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump({"content": content}, file, ensure_ascii=False, indent=4)
        print(f"Сторінка успішно збережена у файл JSON: {json_file}")
    except IOError as e:
        print(f"Помилка збереження у файл JSON: {e}")


def download_and_save_page(url, text_file=None, json_file=None):
    """
    Завантажує сторінку за вказаним URL і зберігає її у текстовий файл та/або JSON файл.

    Параметри:
    - url: URL сторінки для завантаження.
    - text_file: Ім'я текстового файлу для збереження (може бути None).
    - json_file: Ім'я JSON файлу для збереження (може бути None).
    """

    # Вывод текущей рабочей директории
    print("Текущая рабочая директория:", os.getcwd())

    # Завантажуємо сторінку
    content = fetch_page_content(url)

    if content is None:
        return  # При помилці завантаження завершити функцію

    # Збереження у текстовий файл
    if text_file:
        save_to_text_file(content, text_file)

    # Збереження у файл JSON
    if json_file:
        save_to_json_file(content, json_file)


# Використання функції
url = "https://example.com"  # URL сторінки, яку потрібно завантажити
text_file = "page_content.txt"  # Ім'я файлу для текстового збереження, або None
json_file = "page_content.json"  # Ім'я файлу для JSON збереження, або None

download_and_save_page(url, text_file, json_file)
