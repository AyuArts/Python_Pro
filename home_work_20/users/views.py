import logging
import html
from django.contrib.auth.views import PasswordResetView, LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView

from .forms import MyLoginForm, MyRegisterForm, MyPasswordResetForm
from .services import UserManager, BaseFormView, register_user

# Настраиваем логер
logger = logging.getLogger(__name__)

class RegisterView(BaseFormView):
    """
    Представление для регистрации пользователя.
    """
    form_class = MyRegisterForm
    template_name = 'registration/register.html'
    title = "Register New User"
    button_text = "Register"
    action_url_name = 'register'
    extra_links = [
        {'url': reverse_lazy('login'), 'text': 'Already have an account? Log in'}
    ]

    def form_valid(self, form):
        """
        Обработка валидной формы регистрации.
        """
        user = register_user(self.request, form)
        safe_username = html.escape(user.username)
        logger.info(f"New user registered: {safe_username}")
        return redirect(self.get_success_url())


class CustomLoginView(LoginView):
    """
    Кастомное представление для входа.
    """
    authentication_form = MyLoginForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        """
        Обработка валидной формы входа.
        """
        response = super().form_valid(form)
        safe_username = html.escape(self.request.user.username)
        logger.info(f"User {safe_username} logged in.")
        return response

    def form_invalid(self, form):
        """
        Обработка невалидной формы входа.
        """
        username = form.data.get('username', '')
        safe_username = html.escape(username)
        logger.warning(f"Failed login attempt with username: {safe_username}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительных данных в контекст.
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'title': "Login",
            'action_url': self.request.path,
            'button_text': "Log in",
            'extra_links': [
                {'url': reverse_lazy('password_reset'), 'text': 'Forgot password?'},
                {'url': reverse_lazy('register'), 'text': 'Sign up'}
            ]
        })
        return context


class CustomPasswordResetView(PasswordResetView):
    """
    Кастомное представление для восстановления пароля.
    """
    form_class = MyPasswordResetForm
    template_name = 'registration/password_reset.html'

    def form_valid(self, form):
        """
        Обработка валидной формы сброса пароля.
        """
        email = form.cleaned_data['email']
        safe_email = html.escape(email)
        logger.info(f"Password reset requested for email: {safe_email}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительных данных в контекст.
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'title': "Reset Your Password",
            'button_text': "Reset Password",
            'extra_links': [
                {'url': reverse_lazy('login'), 'text': 'Back to login'}
            ]
        })
        return context


class ProfileView(TemplateView):
    """
    Представление для профиля пользователя.
    """
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        """
        Добавление данных о пользователе в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        safe_username = html.escape(self.request.user.username)
        logger.info(f"User {safe_username} accessed their profile.")
        return context
