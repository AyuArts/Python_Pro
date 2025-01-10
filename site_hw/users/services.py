from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from typing import Dict

User = get_user_model()


class UserService:
    """
    Сервис для управления пользователями и аутентификацией.
    """

    @staticmethod
    def register_user(request: HttpRequest, data: Dict[str, str]) -> HttpResponse:
        """
        Регистрирует нового пользователя.

        :param request: HTTP-запрос.
        :param data: Данные формы.
        :return: HTTP-ответ с установленными cookies.
        """
        # Создаем нового пользователя
        user: User = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            age=data.get('age')
        )
        # Выполняем вход и инициализацию сессии и cookies
        response: HttpResponse = UserDataHandler.initialize_user_session_and_cookies(request, user)
        login(request, user)
        return response

    @staticmethod
    def login_user(request: HttpRequest, data: Dict[str, str]) -> HttpResponse:
        """
        Аутентифицирует пользователя и сохраняет данные в cookies и сессии.

        :param request: HTTP-запрос.
        :param data: Данные формы.
        :return: HTTP-ответ с установленными cookies.
        """
        # Аутентификация пользователя
        user: User = authenticate(request, username=data['username'], password=data['password'])
        if not user:
            raise ValidationError("Неверное имя пользователя или пароль.")
        # Выполняем вход и инициализацию сессии и cookies
        response: HttpResponse = UserDataHandler.initialize_user_session_and_cookies(request, user)
        login(request, user)
        return response

    @staticmethod
    def full_logout(request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """
        Полностью выходит из системы и очищает данные в cookies и сессии.
        """
        logout(request)
        UserDataHandler.clear_user_data(response, request)
        return response


class UserDataHandler:
    """
    Класс для работы с cookies и сессиями пользователя.
    """

    @staticmethod
    def initialize_user_session_and_cookies(request: HttpRequest, user: User) -> HttpResponse:
        """
        Инициализирует данные пользователя в cookies и сессии.

        :param request: HTTP-запрос.
        :param user: Объект пользователя.
        :return: HTTP-ответ с установленными cookies.
        """
        response: HttpResponse = HttpResponse()
        UserDataHandler.set_user_data(
            request=request,
            response=response,
            username=user.username,
            age=getattr(user, 'age', None)
        )
        return response

    @staticmethod
    def set_user_data(request: HttpRequest, response: HttpResponse, username: str, age: int = None) -> None:
        """
        Сохраняет имя пользователя в cookies и возраст в сессии.

        :param request: HTTP-запрос.
        :param response: HTTP-ответ.
        :param username: Имя пользователя.
        :param age: Возраст пользователя.
        """
        # Установка данных в cookies
        response.set_cookie('username', username, max_age=3600, path='/')

        # Установка данных в сессии
        if age is not None:
            request.session['age'] = age

    @staticmethod
    def get_user_data(request: HttpRequest) -> Dict[str, str]:
        """
        Получает данные пользователя из cookies и сессии.

        :param request: HTTP-запрос.
        :return: Данные пользователя.
        """
        # Извлекаем имя пользователя из cookies
        username: str = request.COOKIES.get('username', 'Гость')

        # Извлекаем возраст пользователя из сессии
        age: str = request.session.get('age', 'Не указано')

        return {
            'username': username,
            'age': age,
        }

    @staticmethod
    def clear_user_data(response: HttpResponse, request: HttpRequest) -> HttpResponse:
        """
        Удаляет данные пользователя из cookies и сессии.

        :param response: HTTP-ответ.
        :param request: HTTP-запрос.
        :return: Обновленный HTTP-ответ.
        """
        response.delete_cookie('username')
        response.delete_cookie('email')
        request.session.flush()
        return response
