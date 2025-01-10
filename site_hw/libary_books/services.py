from django.db.models import Count, Avg
from django.db import connection
import time
from .models import Author, Book, Review


def fetch_books_for_list(optimize=True):
    """
    Повертає список книг із автором та відгуками.

    :param optimize: Чи використовувати оптимізацію запитів.
    :return: Список книг.
    """
    if optimize:
        return Book.objects.select_related('author').prefetch_related('reviews')
    return Book.objects.all()


# ------------- 3.1. Работа с анотациями и агрегациями (ORM) -------------
def get_sorted_books():
    """
    Возвращает книги, отсортированные по убыванию количества отзывов
    и по убыванию среднего рейтинга.
    """
    return Book.objects.annotate(
        review_count=Count('reviews'),
        average_rating=Avg('reviews__rating')
    ).order_by('-review_count', '-average_rating')


def get_authors_average_rating():
    """
    Возвращает авторов с полем average_rating — средний рейтинг его книг.
    """
    return Author.objects.annotate(
        average_rating=Avg('book__reviews__rating')
    )


def get_books_review_count():
    """
    Возвращает книги с полем review_count — количеством отзывов на каждую книгу.
    """
    return Book.objects.annotate(
        review_count=Count('reviews')
    )


# ------------------- 3.2. Использование Raw SQL -------------------
def get_total_books_count():
    """
    Возвращает общее количество книг в базе данных (через сырой SQL).
    """
    query = "SELECT COUNT(*) FROM libary_books_book"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0


def get_authors_with_popular_books(min_reviews=10):
    """
    Возвращает авторов, у которых есть книги с более чем `min_reviews` отзывами
    (использует сырой SQL с безопасной подстановкой).
    Возвращает список кортежей (id, name, review_count).
    """
    query = """
        SELECT a.id, a.name, COUNT(r.id) AS review_count
        FROM libary_books_author a
        INNER JOIN libary_books_book b ON a.id = b.author_id
        INNER JOIN libary_books_review r ON b.id = r.book_id
        GROUP BY a.id
        HAVING COUNT(r.id) > %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [min_reviews])  # защита от SQL-инъекций
        return cursor.fetchall()
