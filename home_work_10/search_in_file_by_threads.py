"""
Модуль для багатопотокового пошуку тексту у файлі.

Глобальні змінні:
    - counter (int): Лічильник для підрахунку кількості знайдених збігів слова.
    - lock (threading.Lock): Блокування для синхронізації доступу до лічильника між потоками.

Функції:
    - search_in_lines(lines: list, search_text: str) -> None:
        Підраховує кількість входжень шуканого тексту в заданому списку рядків і
        оновлює глобальний лічильник.
    - search_in_file_by_threads(file_path: str, search_text: str, num_threads: int = 4) -> None:
        Розподіляє рядки файлу між потоками і виконує паралельний пошук.
"""

import threading

counter = 0
lock = threading.Lock()

def search_in_lines(lines, search_text):
    """
    Шукає заданий текст у рядках і збільшує глобальний лічильник збігів.

    Аргументи:
        lines (list): Рядки для пошуку.
        search_text (str): Текст для пошуку.
    """
    global counter
    local_counter = sum(line.count(search_text) for line in lines)
    with lock:
        counter += local_counter

def search_in_file_by_threads(file_path, search_text, num_threads=4):
    """
    Розподіляє рядки файлу між потоками для паралельного пошуку тексту.

    Аргументи:
        file_path (str): Шлях до файлу.
        search_text (str): Текст для пошуку.
        num_threads (int): Кількість потоків (за замовчуванням 4).
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=search_in_lines, args=(lines[start:end], search_text))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Загальна кількість входжень '{search_text}': {counter}")


# Виклик функції для пошуку в одному з файлів
search_in_file_by_threads("./downloads/large_file1.txt", "large", num_threads=4)
