from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from celery.result import AsyncResult
from .tasks import import_books_from_csv


def handle_csv_upload(request):
    """
    Обробляє завантаження CSV файлу.

    :param request: HTTP-запит.
    :return: HTTP-відповідь.
    """
    try:
        csv_file = _get_uploaded_file(request)
        file_path = _save_uploaded_file(csv_file)
        task = _start_csv_import_task(file_path, request.user.email)
        messages.success(request, f'Файл успішно завантажено. ID завдання: {task.id}')
        return redirect('task_status', task_id=task.id)
    except ValidationError as ve:
        messages.error(request, str(ve))
    except Exception as e:
        messages.error(request, f'Виникла помилка: {str(e)}')

    return render(request, 'libary_books/upload_csv.html')


def get_task_status_context(task_id):
    """
    Готує контекст для сторінки статусу завдання.

    :param task_id: ID завдання Celery.
    :return: Словник контексту.
    """
    result = AsyncResult(task_id)
    return {
        'task': result,
        'status': result.status,
        'result': result.result if result.successful() else None,
    }


def _get_uploaded_file(request):
    """
    Отримує завантажений файл з запиту.

    :param request: HTTP-запит.
    :return: Завантажений файл.
    :raises ValidationError: Якщо файл не завантажено.
    """
    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        raise ValidationError('Будь ласка, виберіть файл для завантаження.')
    return csv_file


def _save_uploaded_file(csv_file):
    """
    Зберігає завантажений файл у файлову систему.

    :param csv_file: Завантажений файл.
    :return: Шлях до збереженого файлу.
    """
    fs = FileSystemStorage()
    return fs.save(csv_file.name, csv_file)


def _start_csv_import_task(file_path, user_email):
    """
    Запускає завдання імпорту CSV з Celery.

    :param file_path: Шлях до файлу.
    :param user_email: Email користувача для сповіщення.
    :return: Об'єкт завдання Celery.
    """
    return import_books_from_csv.delay(FileSystemStorage().path(file_path), user_email)
