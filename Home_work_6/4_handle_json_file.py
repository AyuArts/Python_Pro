import json


def handle_json_file(json_file, data=None, mode='load'):
    """
    Універсальна функція для завантаження або збереження даних з/до JSON-файлу.

    :param json_file: Шлях до JSON-файлу з даними.
    :param data: Дані для запису (використовується, якщо mode='save').
    :param mode: Режим роботи функції: 'load' для завантаження або 'save' для збереження.
    :return: Список даних із JSON-файлу, якщо режим 'load', або None у режимі 'save'.
    """
    try:
        # Визначаємо режим відкриття файлу ('r' для читання або 'w' для запису)
        file_mode = 'r' if mode == 'load' else 'w'

        with open(json_file, file_mode, encoding='utf-8') as file:
            # Якщо режим 'load', повертаємо завантажені дані
            if mode == 'load':
                return json.load(file)
            # Якщо режим 'save', зберігаємо дані
            elif mode == 'save' and data is not None:
                json.dump(data, file, ensure_ascii=False, indent=4)
            else:
                raise ValueError("Необхідний список даних для збереження у режимі 'save'.")
    except FileNotFoundError:
        print(f"\nФайл '{json_file}' не знайдено.")
        return [] if mode == 'load' else None
    except json.JSONDecodeError:
        print(f"\nПомилка під час читання JSON-файлу '{json_file}'.")
        return [] if mode == 'load' else None


def books_in_stock(json_file):
    """
    Функція завантажує JSON-файл і виводить список книг, які є в наявності.

    :param json_file: Шлях до JSON-файлу з даними про книги.
    """
    books = handle_json_file(json_file, mode='load')

    # Складемо список книг, які є в наявності (наявність == True)
    stock = [book for book in books if book["наявність"]]

    # Якщо немає книг у наявності
    if not stock:
        print("Книг у наявності немає.")
    else:
        # Виводимо інформацію про кожну доступну книгу
        for book in stock:
            print(f"Назва книги: {book['назва']}"
                  f"\nАвтор книги: {book['автор']}"
                  f"\nРік видання: {book['рік']}\n")


def add_book(json_file):
    """
    Функція додає нову книгу до JSON-файлу.

    :param json_file: Шлях до JSON-файлу з даними про книги.
    """
    books = handle_json_file(json_file, mode='load')

    # Введення даних
    name_book = input("Введіть назву книги: ")
    name_author = input("Введіть ім'я автора книги: ")

    # Валідація року видання
    while True:
        try:
            year_of_publication = int(input("Введіть рік видання книги: "))
            break
        except ValueError:
            print("Помилка: Введіть коректний рік числом.")

    # Обробка відповіді про наявність книги
    while True:
        in_stock = input("Книга є в наявності (так/ні)? ").strip().lower()
        if in_stock in ("так", "т", "yes", "y"):
            correct_in_stock = True
            break
        elif in_stock in ("ні", "н", "no", "n"):
            correct_in_stock = False
            break
        else:
            print("Будь ласка, введіть 'так' або 'ні'.")

    # Створюємо нову книгу
    new_book = {
        "назва": name_book,
        "автор": name_author,
        "рік": year_of_publication,
        "наявність": correct_in_stock
    }

    # Додаємо нову книгу до списку
    books.append(new_book)

    # Зберігаємо оновлені дані назад у файл
    handle_json_file(json_file, data=books, mode='save')

    print("Книга успішно додана.")


if __name__ == '__main__':

    # Використання функцій
    json_file = "library.json"

    # Виведення книг, які є в наявності
    books_in_stock(json_file)

    # Додавання нової книги
    add_book(json_file)
