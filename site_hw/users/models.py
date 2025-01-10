from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Кастомна модель користувача з додатковими полями.
    """
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Вік")
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")

    def __str__(self):
        return self.username