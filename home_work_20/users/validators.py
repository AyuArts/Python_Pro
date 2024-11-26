from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from users.models import User


def username_validator(value):
    """
    Проверяет, что имя пользователя состоит только из букв, цифр и символов подчеркивания.
    """
    validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message=_("Username can only contain letters, numbers, and underscores.")
    )
    validator(value)


def unique_email_validator(value):
    """
    Проверяет, что email уникален.
    """
    if User.objects.filter(email=value).exists():
        raise ValidationError(_("This email address is already in use."))


def existing_email_validator(value):
    """
    Проверяет, что email существует в базе данных.
    """
    if not User.objects.filter(email=value).exists():
        raise ValidationError(_("A user with this email address was not found."))
