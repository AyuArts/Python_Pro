from django.urls import path

from .views import (
    BookListViewNoOptimization,
    BookListViewOptimization,
    authors_average_rating,
    books_review_count,
    sorted_books,
    total_books_count,
    authors_with_popular_books,
)

urlpatterns = [
    # Класс-бейз вью:
    path('list/no-optimization/', BookListViewNoOptimization.as_view(), name='book_list_no_optimization'),
    path('list/optimization/', BookListViewOptimization.as_view(), name='books_opt'),

    # Функц. вью:
    path('list/average_rating/', authors_average_rating, name='authors_average_rating'),
    path('list/review_count/', books_review_count, name='books_review_count'),
    path('list/sorted_books/', sorted_books, name='sorted_books'),
    path('list/total_count/', total_books_count, name='total_books_count'),
    path('list/popular_books/', authors_with_popular_books, name='authors_with_popular_books'),
]
