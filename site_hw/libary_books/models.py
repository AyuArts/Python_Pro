from django.db import models

class Author(models.Model):
    """
    Модель автора книги.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель книги с автором и рейтингом.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0, db_index=True)  # Индексация поля rating

    def update_rating(self):
        """
        Обновляет средний рейтинг книги на основе отзывов.
        """
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(review.rating for review in reviews) / reviews.count()
        else:
            self.rating = 0.0
        self.save()

    def __str__(self):
        return f"{self.title} (Rating: {self.rating:.1f})"


class Review(models.Model):
    """
    Модель отзыва на книгу.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        """
        Переопределяем сохранение для обновления рейтинга книги.
        """
        super().save(*args, **kwargs)
        self.book.update_rating()

    def __str__(self):
        return f"Review for {self.book.title} - Rating: {self.rating}/5"
