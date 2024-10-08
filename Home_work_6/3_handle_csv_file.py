import csv


def handle_csv_file(csv_file, data=None, mode='load', fieldnames=None):
    """
    Універсальна функція для завантаження або збереження даних з/до CSV-файлу.

    :param csv_file: Шлях до CSV-файлу.
    :param data: Дані для запису (використовується, якщо mode='save').
    :param mode: Режим роботи функції: 'load' для завантаження або 'save' для збереження.
    :param fieldnames: Список заголовків стовпців (використовується для writer).
    :return: Список рядків із CSV-файлу, якщо режим 'load', або None у режимі 'save'.
    """
    try:
        # Визначаємо режим відкриття файлу ('r' для читання або 'w' для запису)
        file_mode = 'r' if mode == 'load' else 'w'

        with open(csv_file, file_mode, encoding='utf-8', newline='') as file:
            if mode == 'load':
                # Якщо режим 'load', завантажуємо дані з файлу за допомогою DictReader
                reader = csv.DictReader(file)
                return list(reader)
            elif mode == 'save' and data is not None:
                # Якщо режим 'save', зберігаємо дані до файлу за допомогою DictWriter
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                raise ValueError("Необхідний список даних для збереження у режимі 'save'.")
    except FileNotFoundError:
        print(f"\nФайл '{csv_file}' не знайдено.")
        return [] if mode == 'load' else None
    except csv.Error:
        print(f"\nПомилка під час читання або запису CSV-файлу '{csv_file}'.")
        return [] if mode == 'load' else None


def students_display(csv_file):
    """
    Функція завантажує CSV-файл і виводить список студентів.

    :param csv_file: Шлях до CSV-файлу з даними про студентів.
    """
    students = handle_csv_file(csv_file, mode='load')

    # Якщо немає студентів
    if not students:
        print("Студентів немає.")
    else:
        # Виводимо інформацію про кожного студента
        for student in students:
            print(f"Ім'я студента: {student['Ім\'я']}"
                  f"\nВік студента: {student['Вік']}"
                  f"\nОцінка студента: {student['Оцінка']}\n")


def add_student(csv_file):
    """
    Функція додає нового студента до CSV-файлу.

    :param csv_file: Шлях до CSV-файлу з даними про студентів.
    """
    students = handle_csv_file(csv_file, mode='load')

    # Введення даних
    name = input("Введіть ім'я студента: ")
    age = input("Введіть вік студента: ")

    # Валідація оцінки
    while True:
        try:
            grade = int(input("Введіть оцінку студента: "))
            break
        except ValueError:
            print("Помилка: Введіть коректну оцінку числом.")

    # Створюємо нового студента
    new_student = {
        "Ім'я": name,
        "Вік": age,
        "Оцінка": grade
    }

    # Додаємо нового студента до списку
    students.append(new_student)

    # Зберігаємо оновлені дані назад у файл
    fieldnames = ["Ім'я", "Вік", "Оцінка"]
    handle_csv_file(csv_file, data=students, mode='save', fieldnames=fieldnames)

    print("Новий студент успішно доданий.")


if __name__ == '__main__':

    # Шлях до CSV-файлу
    csv_file = "students.csv"

    # 1. Виведення студентів, які є в списку
    students_display(csv_file)

    # 2. Додавання нового студента
    add_student(csv_file)
