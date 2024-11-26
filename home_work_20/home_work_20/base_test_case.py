from django.test import TestCase
from django.utils import timezone

from users.models import User


class BaseTestCase(TestCase):
    """Базовый тестовый класс"""

    def create_user(self):
        """Создает и возвращает тестового пользователя"""
        username = self.get_valid_data(name_data="user")["username"]
        email = self.get_valid_data(name_data="user")["email"]
        password = self.get_valid_data(name_data="user")["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    @staticmethod
    def get_afterworld(days=1):
        """Возвращает данные с датой в будущем"""
        return (timezone.now() + timezone.timedelta(days=days)).date()

    def get_valid_data(self, name_data):
        """Создает и возвращает валидные данные для тестов"""
        if name_data == "task":
            return {
                'title': 'Test Task',
                'description': 'This is a test description.',
                'done': False,
                'due_date': self.get_afterworld(),
                'user': self.create_user().id,
            }
        elif name_data == "user":
            return {
                'username': 'test',
                'email': 'test@test.com',
                'password': '12345678Test',
            }



    def get_past_date_data(self, days=1):
        """Возвращает данные с датой в прошлом"""
        data = self.get_valid_data(name_data="task")
        data['due_date'] = (timezone.now() - timezone.timedelta(days=days)).date()
        return data

    def get_missing_title_data(self):
        """Возвращает данные с пустым заголовком"""
        data = self.get_valid_data(name_data="task")
        data['title'] = ""
        return data