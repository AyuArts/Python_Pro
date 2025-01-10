import random
from libary_books.models import Author, Book, Review

def populate_test_data():
    """
    Скрипт для заполнения базы данных тестовыми авторами, книгами и отзывами с рейтингами.
    """
    # Создание авторов
    authors = []
    for i in range(10):  # Добавить 10 авторов
        author = Author.objects.create(
            name=f"Автор {i+1}"
        )
        authors.append(author)

    # Создание книг
    books = []
    for i in range(50):  # Добавить 50 книг
        book = Book.objects.create(
            title=f"Книга {i+1}",
            author=random.choice(authors)
        )
        books.append(book)

    # Создание отзывов с рейтингами
    for book in books:
        for _ in range(random.randint(1, 5)):  # Случайное количество отзывов (1-5) для каждой книги
            rating = random.randint(1, 5)  # Рейтинг от 1 до 5
            Review.objects.create(
                book=book,
                content=f"Это отзыв на книгу '{book.title}'.",
                rating=rating
            )
        # Обновление рейтинга книги после добавления всех отзывов
        book.update_rating()

    print("Тестовые данные успешно добавлены в базу данных.")
