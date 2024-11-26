from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.validators import username_validator, unique_email_validator, existing_email_validator

User = get_user_model()


class BaseStyledFormMixin:
    """
    Базовый миксин для добавления общих стилей и атрибутов к виджетам.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                placeholder = field.widget.attrs.get("placeholder", f"Enter your {field_name}")
                field.widget.attrs.setdefault("placeholder", placeholder)


class MyLoginForm(BaseStyledFormMixin, AuthenticationForm):
    """
    Кастомная форма для входа.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": _("Enter your username")})
        self.fields['password'].widget.attrs.update({"placeholder": _("Enter your password")})


class MyRegisterForm(BaseStyledFormMixin, UserCreationForm):
    """
    Кастомная форма для регистрации.
    """

    username = forms.CharField(
        max_length=150,
        validators=[username_validator],
        widget=forms.TextInput(attrs={"placeholder": _("Enter your username")}),
    )

    email = forms.EmailField(
        required=True,
        validators=[unique_email_validator],
        widget=forms.EmailInput(attrs={"placeholder": _("Enter your email")}),
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("Enter your password"), "id": "id_password1"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("Repeat your password"), "id": "id_password2"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MyPasswordChangeForm(BaseStyledFormMixin, PasswordChangeForm):
    """
    Кастомная форма для смены пароля.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({"placeholder": _("Enter your current password")})
        self.fields['new_password1'].widget.attrs.update({"placeholder": _("Enter your new password")})
        self.fields['new_password2'].widget.attrs.update({"placeholder": _("Confirm your new password")})


class MyPasswordResetForm(BaseStyledFormMixin, PasswordResetForm):
    """
    Кастомная форма для восстановления пароля.
    """
    email = forms.EmailField(
        validators=[existing_email_validator],
        widget=forms.EmailInput(attrs={"placeholder": _("Enter your email")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MySetPasswordForm(BaseStyledFormMixin, SetPasswordForm):
    """
    Кастомная форма для установки нового пароля.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"placeholder": _("Enter your new password")})
        self.fields['new_password2'].widget.attrs.update({"placeholder": _("Confirm your new password")})


class MyEmailChangeForm(BaseStyledFormMixin, forms.ModelForm):
    """
    Кастомная форма для изменения email.
    """

    email = forms.EmailField(
        validators=[unique_email_validator],
        widget=forms.EmailInput(attrs={"placeholder": _("Enter your new email")}),
    )

    class Meta:
        model = User
        fields = ["email"]
