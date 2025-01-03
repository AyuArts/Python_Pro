from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    """
    Модель для представлення користувачів.

    :param id: Унікальний ідентифікатор користувача.
    :param username: Ім'я користувача.
    :param email: Електронна пошта користувача.
    :param password_hash: Хешований пароль.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Director(db.Model):
    """
    Модель для представлення режисерів.

    :param id: Унікальний ідентифікатор режисера.
    :param name: Ім'я режисера.
    """
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    films = db.relationship('Film', backref='director', lazy='dynamic')

    def to_dict(self):
        """
        Повертає словник з інформацією про режисера.

        :return: Словник з id та name режисера.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        """
        Повертає строкове представлення об'єкта Director.

        :return: Ім'я режисера.
        """
        return f'Director {self.name}'


class Film(db.Model):
    """
    Модель для представлення фільмів.

    :param id: Унікальний ідентифікатор фільму.
    :param title: Назва фільму.
    :param release_year: Рік виходу фільму.
    :param rating: Рейтинг фільму.
    :param description: Опис фільму.
    :param director_id: ID режисера (зовнішній ключ).
    """
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)

    def to_dict(self):
        """
        Повертає словник з інформацією про фільм.

        :return: Словник з даними про фільм.
        """
        return {
            "id": self.id,
            "title": self.title,
            "release_year": self.release_year,
            "rating": self.rating,
            "description": self.description,
            "director_id": self.director_id,
            "director_name": self.director.name if self.director else None
        }

    def __repr__(self):
        """
        Повертає строкове представлення об'єкта Film.

        :return: Назва фільму.
        """
        return f'Film {self.title}'
