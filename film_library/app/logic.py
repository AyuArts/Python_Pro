from app.models import Film, Director
from app.extensions import db


# Вспомогательные функции
def get_object_or_404(model, object_id):
    """Получает объект по ID или выбрасывает 404 ошибку."""
    obj = model.query.get(object_id)
    if not obj:
        raise ValueError(f"{model.__name__} with ID {object_id} not found.")
    return obj


def save_to_db(obj):
    """Сохраняет объект в базу данных."""
    db.session.add(obj)
    db.session.commit()
    return obj


def delete_from_db(obj):
    """Удаляет объект из базы данных."""
    db.session.delete(obj)
    db.session.commit()


def update_object_from_data(obj, data, fields):
    """
    Обновляет атрибуты объекта из словаря.

    :param obj: Объект для обновления.
    :param data: Данные в формате словаря.
    :param fields: Словарь полей и их типов для приведения данных.
    """
    for field, cast_type in fields.items():
        if field in data:
            setattr(obj, field, cast_type(data[field]))
    return obj


# Основная логика
def create_director(name):
    """Создаёт нового режиссёра."""
    return save_to_db(Director(name=name))


def get_all_directors():
    """Возвращает список всех режиссёров."""
    return Director.query.all()


def update_director_by_id(director_id, name):
    """Обновляет имя режиссёра по ID."""
    director = get_object_or_404(Director, director_id)
    if name:
        director.name = name
        db.session.commit()
    return director


def delete_director_by_id(director_id):
    """Удаляет режиссёра и переназначает его фильмы."""
    director = get_object_or_404(Director, director_id)
    unknown = Director.query.filter_by(name="unknown").first()
    for film in director.films:
        film.director_id = unknown.id
    delete_from_db(director)


def create_film(data):
    """Создаёт новый фильм."""
    fields_to_cast = {
        'title': str,
        'release_year': int,
        'rating': float,
        'director_id': int,
    }
    film_data = {key: fields_to_cast[key](data[key]) for key in fields_to_cast}
    return save_to_db(Film(**film_data))


def get_all_films():
    """Возвращает список всех фильмов."""
    return Film.query.all()


def update_film_by_id(film_id, data):
    """Обновляет данные фильма по ID."""
    film = get_object_or_404(Film, film_id)
    fields_to_update = {
        'title': str,
        'release_year': int,
        'rating': float,
        'description': str,
    }
    film = update_object_from_data(film, data, fields_to_update)

    if 'director_id' in data:
        director = get_object_or_404(Director, data['director_id'])
        film.director_id = director.id

    db.session.commit()
    return film


def delete_film_by_id(film_id):
    """Удаляет фильм по ID."""
    film = get_object_or_404(Film, film_id)
    delete_from_db(film)
