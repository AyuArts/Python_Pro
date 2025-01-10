from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label="Ваше ім'я", max_length=100)
    age = forms.IntegerField(label="Ваш вік", min_value=1, required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """
    Форма для реєстрації користувача.
    """
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label="Підтвердження паролю", widget=forms.PasswordInput)
    age = forms.IntegerField(label="Ваш вік", min_value=1, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """
        Перевірка валідності форми: підтвердження паролю.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Паролі не співпадають.')

        return cleaned_data

    def clean_username(self):
        """
        Перевіряє унікальність імені користувача.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Користувач із таким ім\'ям вже існує.')
        return username

    def clean_email(self):
        """
        Перевіряє унікальність електронної пошти.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Користувач із такою електронною поштою вже існує.')
        return email

