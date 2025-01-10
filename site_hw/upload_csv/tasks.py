import csv
import os
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from libary_books.models import Book, Author

logger = logging.getLogger(__name__)


class CSVImporter:
    """
    Класс для импорта книг из файла CSV.
    """

    def __init__(self, file_path, user_email):
        """
        Инициализация CSVImporter.

        :param file_path: Путь к файлу CSV.
        :param user_email: Email пользователя для уведомления.
        """
        self.file_path = file_path
        self.user_email = user_email

    def validate_csv_structure(self, reader):
        """
        Проверяет структуру CSV.

        :param reader: CSV reader объект.
        :raises ValueError: Если структура неверная.
        """
        required_fields = {'title', 'author'}
        if not required_fields.issubset(reader.fieldnames):
            raise ValueError(f"CSV файл должен содержать колонки: {', '.join(required_fields)}")

    def process_row(self, row):
        """
        Обрабатывает одну строку из CSV.

        :param row: Строка CSV в виде словаря.
        """
        author, _ = Author.objects.get_or_create(name=row['author'])
        Book.objects.create(
            title=row['title'],
            author=author,
        )

    def import_csv(self):
        """
        Импортирует книги из CSV в базу данных.
        """
        with open(self.file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            self.validate_csv_structure(reader)
            for row in reader:
                try:
                    self.process_row(row)
                except Exception as e:
                    logger.error(f"Ошибка при обработке строки {row}: {e}")

    def send_notification(self):
        """
        Отправляет email уведомление пользователю.
        """
        send_mail(
            'Импорт завершён',
            'Ваш импорт данных из CSV был успешно завершён.',
            'aaslyamov.arts@gmail.com',
            [self.user_email],
            fail_silently=False,
        )

    def cleanup(self):
        """
        Удаляет временный файл.
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


@shared_task
def import_books_from_csv(file_path, user_email):
    """
    Асинхронная задача для импорта книг из файла CSV.
    """
    importer = CSVImporter(file_path, user_email)
    try:
        importer.import_csv()
        importer.send_notification()
    except Exception as e:
        logger.error(f"Ошибка при выполнении задачи: {e}")
    finally:
        importer.cleanup()
