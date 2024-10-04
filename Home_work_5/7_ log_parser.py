import os

class LogErrorIterator:
    """
    Ітератор для проходження через лог-файл і вибору тільки рядків з помилками (4XX або 5XX статуси).

    :param file_path: Шлях до лог-файлу.
    :type file_path: str
    """

    def __init__(self, file_path: str):
        """
        Ініціалізує ітератор з шляхом до лог-файлу.

        :param file_path: Шлях до лог-файлу.
        :type file_path: str
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не існує")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file_path} не є файлом")

        self.file_path = file_path
        self.file = open(file_path, 'r', encoding='utf-8')  # Відкриваємо файл для читання
        self.current_line = None

    def __iter__(self):
        """
        Повертає ітератор для рядків з помилками у лог-файлі.

        :return: Ітератор для рядків з помилками.
        :rtype: iterator
        """
        return self

    def __next__(self):
        """
        Повертає наступний рядок з помилкою (код статусу 4XX або 5XX).

        :return: Рядок з лог-файлу, що містить помилку.
        :rtype: str
        """
        for line in self.file:
            parts = line.split()
            if len(parts) > 8:
                status_code = parts[8]
                if status_code.startswith('4') or status_code.startswith('5'):
                    return line
        raise StopIteration

    def close(self):
        """
        Закриває файл після завершення ітерації.
        """
        self.file.close()


def save_errors_to_file(input_file: str, output_file: str):
    """
    Зберігає рядки з помилками у окремий файл.

    :param input_file: Шлях до вхідного файлу логів.
    :param output_file: Шлях для збереження помилок.
    """
    try:
        log_iterator = LogErrorIterator(input_file)

        with open(output_file, 'w', encoding='utf-8') as error_file:
            for error_line in log_iterator:
                error_file.write(error_line)

        print(f"Помилки збережено у файл: {output_file}")
        log_iterator.close()

    except (FileNotFoundError, IOError) as e:
        print(e)


# Запит шляху до лог-файлу у користувача
log_file_path = input("Введіть шлях до лог-файлу: ").strip()

# Якщо шлях не вказано, використовуємо поточний каталог
if not log_file_path or log_file_path == '.':
    log_file_path = os.getcwd()

# Перетворюємо відносний шлях на абсолютний, якщо необхідно
if not os.path.isabs(log_file_path):
    log_file_path = os.path.abspath(log_file_path)

# Встановлюємо шлях для збереження помилок
output_error_file = os.path.join(os.path.dirname(log_file_path), 'errors.log')

# Виклик функції для збереження помилок у файл
save_errors_to_file(log_file_path, output_error_file)
