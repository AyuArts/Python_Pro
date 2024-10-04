import zipfile
import os

class ZipManager:
    """
    Контекстний менеджер для архівування файлів.

    :param zip_file_path: Шлях до архіву, який створюється.
    :type zip_file_path: str
    """

    def __init__(self, zip_file_path: str):
        """
        Ініціалізує контекстний менеджер з шляхом до архіву.

        :param zip_file_path: Шлях до архіву.
        :type zip_file_path: str
        """
        self.zip_file_path = zip_file_path
        self.zip_file = None

    def __enter__(self):
        """
        Відкриває архів для запису файлів при вході в контекст.

        :return: Об'єкт ZipFile для додавання файлів.
        :rtype: zipfile.ZipFile
        """
        self.zip_file = zipfile.ZipFile(self.zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        print(f"Архів створено: {self.zip_file_path}")
        return self.zip_file

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закриває архів при виході з контексту.

        :param exc_type: Тип винятку.
        :param exc_value: Значення винятку.
        :param traceback: Слідова інформація про виняток.
        """
        if self.zip_file:
            self.zip_file.close()
            print(f"Архів закрито: {self.zip_file_path}")

# Використання контекстного менеджера для архівування файлів

zip_file = 'archive.zip'

with ZipManager(zip_file) as zip_archive:
    # Додаємо файли до архіву
    zip_archive.write('file1.txt')
    zip_archive.write('file2.txt')

# Архів буде автоматично закрито після виходу з контексту
