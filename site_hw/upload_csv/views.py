from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CSVUploadForm
from celery.result import AsyncResult
from django.http import JsonResponse
from .tasks import import_books_from_csv
import os
from django.conf import settings


def upload_csv(request):
    """
    Загрузка CSV-файла для импорта данных.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

            # Сохраняем файл в директорию MEDIA или TEMP
            upload_dir = os.path.join(settings.BASE_DIR, 'uploaded_files')
            os.makedirs(upload_dir, exist_ok=True)  # Создаём директорию, если её нет
            file_path = os.path.join(upload_dir, csv_file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Запуск задачи Celery
            task = import_books_from_csv.delay(file_path, request.user.email)
            return redirect(reverse('task_status', kwargs={'task_id': task.id}))
    else:
        form = CSVUploadForm()
    return render(request, 'libary_books/upload_csv.html', {'form': form})


def task_status(request, task_id):
    """
    Отображение статуса задачи.
    """
    task = AsyncResult(task_id)
    return render(request, 'libary_books/task_status.html', {'task': task})