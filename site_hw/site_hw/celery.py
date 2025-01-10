from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_hw.settings')

app = Celery('site_hw')

# Используйте настройки Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

# Настройки Celery для Windows
app.conf.update(
    worker_pool='solo',
    broker_connection_retry_on_startup=True,
)

# Проверка задач
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
