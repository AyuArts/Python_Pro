import time
import functools
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View

from .services import (
    fetch_books_for_list,
    get_sorted_books,
    get_authors_average_rating,
    get_books_review_count,
    get_total_books_count,
    get_authors_with_popular_books,
)


def measure_execution_time(view_func):
    """
    Универсальный декоратор, который корректно обрабатывает:
    1) Метод класса (первый аргумент будет self, второй — request),
    2) Обычную функц. вью (первый аргумент — request).
    """
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = view_func(*args, **kwargs)
        execution_time = round((time.time() - start_time) * 1000, 2)
        print(f"Execution time for {view_func.__name__}: {execution_time}ms")
        return response
    return wrapper


class BaseBookListView(View):
    """
    Базовый класс для отображения списка книг.
    """

    template_name: str = None  # Шаблон для рендеринга
    optimization: bool = False  # Оптимизировать запросы или нет
    cache_timeout: int = 0  # Время кеширования в секундах (0 = не кешировать)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.cache_timeout > 0:
            # Автоматическое применение кеширования к dispatch
            self.dispatch = method_decorator(cache_page(self.cache_timeout))(self.dispatch)

    @method_decorator(measure_execution_time)
    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для отображения списка книг.

        :param request: HTTP-запрос.
        :return: HTTP-ответ с рендерингом списка книг.
        """
        books = fetch_books_for_list(optimize=self.optimization)
        return render(request, self.template_name, {'books': books})


class BookListViewOptimization(BaseBookListView):
    """
    Отображение списка книг с оптимизацией запросов.
    """
    template_name = 'libary_books/book_list_optimization.html'
    optimization = True
    cache_timeout = 900 # Кеш на 15 минут


class BookListViewNoOptimization(BaseBookListView):
    """
    Отображение списка книг без оптимизации запросов.
    """
    template_name = 'libary_books/book_list_no_optimization.html'
    optimization = False
    cache_timeout = 0  # Без кеширования


@measure_execution_time
def sorted_books(request):
    """
    Відображення книг, відсортованих за кількістю відгуків та середнім рейтингом.
    """
    books = get_sorted_books()
    return render(request, 'libary_books/sorted_books.html', {'books': books})


@measure_execution_time
def authors_average_rating(request):
    """
    Відображення середнього рейтингу книг кожного автора.
    """
    authors = get_authors_average_rating()
    return render(request, 'libary_books/average_rating.html', {'authors': authors})


@measure_execution_time
def books_review_count(request):
    """
    Відображення кількості відгуків кожної книги.
    """
    books = get_books_review_count()
    return render(request, 'libary_books/review_count.html', {'books': books})


@measure_execution_time
def total_books_count(request):
    """
    Відображення загальної кількості книг у базі даних.
    """
    total_books = get_total_books_count()
    return render(request, 'libary_books/total_count.html', {'total_books': total_books})


@measure_execution_time
def authors_with_popular_books(request):
    """
    Відображення авторів із популярними книгами.
    """
    results = get_authors_with_popular_books()
    return render(request, 'libary_books/popular_books.html', {'results': results})
