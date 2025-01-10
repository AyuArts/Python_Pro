from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver
from .models import Book


@receiver(post_save, sender=Book)
def clear_book_list_cache(sender, instance, **kwargs):
    """
    Очищает кеш списка книг после изменения или добавления книги.
    """
    cache.delete_pattern('anon_cache_*')  # Удаляем все связанные кеши
