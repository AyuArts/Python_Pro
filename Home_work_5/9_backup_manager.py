import os
import shutil

class BackupManager:
    """
    Контекстний менеджер для створення резервної копії файлу перед його обробкою.

    :param file_path: Шлях до файлу, який обробляється.
    :type file_path: str
    """

    def __init__(self, file_path: str):
        """
        Ініціалізує контекстний менеджер з шляхом до файлу.

        :param file_path: Шлях до файлу.
        :type file_path: str
        """
        self.file_path = file_path
        self.backup_path = f"{file_path}.bak"

    def __enter__(self):
        """
        Створює резервну копію файлу при вході в контекст.

        :return: Шлях до файлу для обробки.
        :rtype: str
        """
        # Створюємо резервну копію файлу
        shutil.copy(self.file_path, self.backup_path)
        print(f"Резервну копію створено: {self.backup_path}")
        return self.file_path

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Якщо обробка завершилася успішно, оригінальний файл оновлюється.
        У разі помилки резервна копія відновлюється.

        :param exc_type: Тип винятку.
        :param exc_value: Значення винятку.
        :param traceback: Слідова інформація про виняток.
        """
        if exc_type is None:
            # Обробка пройшла успішно, резервну копію можна видалити
            os.remove(self.backup_path)
            print("Оригінальний файл оновлено, резервну копію видалено.")
        else:
            # У разі помилки відновлюємо файл з резервної копії
            shutil.copy(self.backup_path, self.file_path)
            os.remove(self.backup_path)
            print("Виникла помилка! Файл відновлено з резервної копії.")

# Використання контекстного менеджера для обробки файлу

file_path = 'important_file.txt'

try:
    with BackupManager(file_path) as file:
        # Обробляємо файл (наприклад, змінюємо його вміст)
        with open(file, 'w') as f:
            f.write("Новий вміст файлу.\n")
except Exception as e:
    print(f"Помилка: {e}")
