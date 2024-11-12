from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    """
    Модель для представления категории объявлений.

    Атрибуты:
    ----------
    name : str
        Название категории, уникальное поле.
    description : str
        Краткое описание категории (опционально).
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def active_ads_count(self):
        """
        Возвращает количество активных объявлений в категории.

        :return: Количество активных объявлений.
        :rtype: int
        """
        return self.ad_set.filter(is_active=True).count()

    def __str__(self):
        """
        Возвращает строковое представление категории.

        :return: Название категории.
        :rtype: str
        """
        return self.name


class Ad(models.Model):
    """
    Модель для представления объявления.

    Атрибуты:
    ----------
    title : str
        Заголовок объявления.
    description : str
        Описание объявления.
    price : Decimal
        Цена объявления, должна быть положительным числом.
    created_at : datetime
        Дата и время создания объявления.
    updated_at : datetime
        Дата и время последнего обновления объявления.
    is_active : bool
        Статус активности объявления.
    user : User
        Владелец объявления.
    category : Category
        Категория, к которой относится объявление.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Сохраняет объект после проверки, что цена положительная.

        :raises ValidationError: Если цена неположительная.
        """
        if self.price <= 0:
            raise ValidationError("Ціна повинна бути додатною")
        super().save(*args, **kwargs)

    def short_description(self):
        """
        Возвращает краткое описание объявления (до 100 символов).

        :return: Краткое описание.
        :rtype: str
        """
        return self.description[:100]

    def deactivate_after_30_days(self):
        """
        Деактивирует объявление, если прошло 30 дней с момента его создания.
        """
        if (timezone.now() - self.created_at).days >= 30:
            self.is_active = False
            self.save()

    def __str__(self):
        """
        Возвращает строковое представление объявления.

        :return: Заголовок объявления.
        :rtype: str
        """
        return self.title


class Comment(models.Model):
    """
    Модель для представления комментария к объявлению.

    Атрибуты:
    ----------
    content : str
        Текст комментария.
    created_at : datetime
        Дата и время создания комментария.
    ad : Ad
        Объявление, к которому относится комментарий.
    user : User
        Пользователь, оставивший комментарий.
    """

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление комментария.

        :return: Информация о пользователе и объявлении, к которому относится комментарий.
        :rtype: str
        """
        return f'Comment by {self.user} on {self.ad}'
