"""
Модуль для завантаження даних з JSON-файлів з використанням кешу для покращення продуктивності.

Використовується функція `load_json` для завантаження та кешування даних з JSON-файлів.
"""

import json

# Кеш для збереження завантажених JSON-файлів, щоб уникнути повторного читання з диску
_json_cache = {}


def load_json(file_path):
    """
    Завантажує дані з JSON-файлу з використанням кешу для покращення продуктивності.

    Якщо JSON-файл вже був завантажений раніше, функція повертає дані з кешу.
    Інакше, вона читає файл з диску, завантажує його в пам'ять та зберігає в кеші.

    :param file_path: Шлях до JSON-файлу, який потрібно завантажити.
    :type file_path: str
    :return: Дані, завантажені з JSON-файлу.
    :rtype: dict або list
    :raises FileNotFoundError: Якщо файл не знайдено за вказаним шляхом.
    :raises json.JSONDecodeError: Якщо файл не є валідним JSON.
    """
    if file_path not in _json_cache:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                _json_cache[file_path] = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл не знайдено: {file_path}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Помилка декодування JSON у файлі: {file_path}", e.doc, e.pos) from e
    return _json_cache[file_path]
