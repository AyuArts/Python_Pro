from django.contrib.auth import login
from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


def register_user(request, form):
    """
    Логика регистрации пользователя.
    """
    user = form.save()
    login(request, user)
    return user

class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)





class BaseFormView(View):
    """
    Базовый класс для работы с формами.
    """
    form_class = None
    template_name = None
    title = None
    button_text = None
    action_url_name = None
    extra_links = None

    def get_context_data(self, form):
        """
        Создание контекста для передачи в шаблон.
        """
        return {
            'form': form,
            'title': self.title,
            'action_url': reverse_lazy(self.action_url_name),
            'button_text': self.button_text,
            'extra_links': self.extra_links or []
        }

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для отображения формы.
        """
        form = self.form_class()
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса для валидации формы.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def form_valid(self, form):
        """
        Должен быть реализован в подклассах.
        """
        raise NotImplementedError("Subclasses must implement form_valid.")

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешной обработки.
        """
        return reverse_lazy('home')