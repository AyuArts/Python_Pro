from django.contrib import admin
from .models import Category, Ad, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс админ-панели для модели Category.

    Атрибуты:
    ----------
    list_display : tuple
        Поля, которые будут отображаться в списке категорий в админ-панели.
    """

    list_display = ('name', 'description')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Класс админ-панели для модели Ad.

    Атрибуты:
    ----------
    list_display : tuple
        Поля, которые будут отображаться в списке объявлений в админ-панели.
    list_filter : tuple
        Поля, по которым можно фильтровать объявления.
    search_fields : tuple
        Поля, по которым можно выполнять поиск в админ-панели.
    """

    list_display = ('title', 'price', 'is_active', 'user', 'category', 'created_at')

