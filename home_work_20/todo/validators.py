from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_due_date(due_date):
    """
    Проверяет, чтобы дата не была в прошлом.

    :param due_date: Дата выполнения задачи
    :raises ValidationError: Если дата в прошлом
    """
    if due_date and due_date < timezone.now().date():
        raise ValidationError("Due date cannot be in the past.")