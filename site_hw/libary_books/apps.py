from django.apps import AppConfig


class LibaryBooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libary_books'

    def ready(self):
        import libary_books.signals
