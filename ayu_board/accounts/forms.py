from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User  # Імпортуємо модель User
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    """
    Форма для реєстрації нового користувача.

    Поля:
    - username: Ім'я користувача
    - email: Електронна адреса користувача
    - password: Пароль користувача
    - password_confirm: Поле для підтвердження паролю

    Методи:
    - clean_email: Перевіряє, чи існує користувач із вказаною електронною адресою.
    - clean: Перевіряє, чи співпадають пароль та його підтвердження.
    """
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Підтвердження паролю")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        """
        Перевірка електронної пошти на унікальність.

        :return: Електронна адреса, якщо вона унікальна
        :rtype: str
        :raises ValidationError: Якщо користувач із вказаною поштою вже існує
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою електронною поштою вже існує.")
        return email

    def clean(self):
        """
        Загальна перевірка форми. Перевіряє, чи співпадають пароль і підтвердження.

        :raises ValidationError: Якщо паролі не співпадають
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Паролі не співпадають.")


class UserProfileForm(ModelForm):
    """
    Форма для редагування профілю користувача.

    Поля:
    - bio: Опис профілю
    - birth_date: Дата народження
    - location: Місцезнаходження
    - avatar: Аватар користувача

    Методи:
    - clean_avatar: Перевіряє розмір завантаженого аватару.
    """
    class Meta:
        model = UserProfile
        fields = ('bio', 'birth_date', 'location', 'avatar')

    def clean_avatar(self):
        """
        Перевірка розміру аватару.

        :return: Завантажений файл аватару
        :rtype: InMemoryUploadedFile
        :raises ValidationError: Якщо розмір файлу перевищує 2 МБ
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("Розмір зображення не повинен перевищувати 2 МБ.")
        return avatar


class PasswordChangeForm(AuthPasswordChangeForm):
    """
    Форма для зміни паролю користувача.

    Поля:
    - old_password: Поточний пароль
    - new_password1: Новий пароль
    - new_password2: Підтвердження нового паролю

    Методи:
    - clean_new_password1: Перевіряє, щоб новий пароль відрізнявся від поточного.
    """
    old_password = forms.CharField(widget=forms.PasswordInput, label="Поточний пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новий пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Підтвердження нового паролю")

    def clean_new_password1(self):
        """
        Перевірка нового паролю. Новий пароль повинен відрізнятися від поточного.

        :return: Новий пароль
        :rtype: str
        :raises ValidationError: Якщо новий пароль збігається з поточним
        """
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        if old_password == new_password1:
            raise ValidationError("Новий пароль повинен відрізнятися від поточного.")
        return new_password1
