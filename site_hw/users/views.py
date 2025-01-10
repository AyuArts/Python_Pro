from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from typing import Type, Optional

from .forms import LoginForm, RegisterForm
from .services import UserService, UserDataHandler


class BaseAuthView(View):
    """
    Базовое представление для аутентификации пользователей.
    """

    form_class: Type[LoginForm | RegisterForm] = None
    template_name: str = None
    success_url: str = '/welcome/'
    auth_key: Optional[str] = None

    def get_form(self, request: HttpRequest):
        """
        Возвращает объект формы.

        :param request: HTTP-запрос.
        :return: Объект формы для обработки данных.
        """
        return self.form_class(request.POST or None)

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Обработка GET-запроса: отображение формы.

        :param request: HTTP-запрос.
        :return: HTTP-ответ с рендерингом формы.
        """
        form = self.get_form(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form(request)
        if form.is_valid():
            if self.auth_key == 'login':
                response = UserService.login_user(request, form.cleaned_data)
            elif self.auth_key == 'register':
                response = UserService.register_user(request, form.cleaned_data)

            response['Location'] = self.success_url
            response.status_code = 302
            return response
        else:
            messages.error(request, form.errors)

            return render(request, self.template_name, {'form': form})


class RegisterView(BaseAuthView):
    """
    Представление для регистрации пользователя.
    """
    form_class = RegisterForm
    template_name = 'users/register.html'
    auth_key = 'register'


class LoginView(BaseAuthView):
    """
    Представление для входа пользователя.
    """
    form_class = LoginForm
    template_name = 'users/login.html'
    auth_key = 'login'


class WelcomeView(View):
    """
    Представление для отображения страницы приветствия.
    """
    template_name = 'users/welcome.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Получает данные пользователя из cookies и сессии.

        :param request: HTTP-запрос.
        :return: HTTP-ответ с рендерингом приветственной страницы.
        """
        user_data = UserDataHandler.get_user_data(request)
        return render(request, self.template_name, user_data)


class LogoutView(View):
    """
    Представление для выхода пользователя.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Обрабатывает выход пользователя из системы.

        :param request: HTTP-запрос.
        :return: HTTP-ответ с редиректом на страницу входа.
        """
        response = redirect('login')
        UserService.full_logout(request, response)
        messages.success(request, "Вы успешно вышли из системы.")
        return response
