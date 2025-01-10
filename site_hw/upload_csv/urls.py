from django.urls import path
from .views import upload_csv, task_status

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('task-status/<str:task_id>/', task_status, name='task_status'),
]
