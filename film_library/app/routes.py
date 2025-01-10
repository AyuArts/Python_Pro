from flask import Blueprint, jsonify
from app.logic import *
from app.models import Director
from app.utils import validate_input, handle_exceptions, serialize_objects, success_message
from app.database import seed_database

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return {"message": "Welcome to the Film Library API"}


@main.route('/directors', methods=['POST'])
@handle_exceptions
@validate_input(['name'])
def add_director(data):
    """Adds a new director."""
    director = create_director(data['name'])
    return jsonify(director.to_dict()), 201


@main.route('/directors', methods=['GET'])
@handle_exceptions
def get_directors():
    """Gets a list of all directors."""
    directors = get_all_directors()
    return jsonify(serialize_objects(directors)), 200


@main.route('/directors/<int:director_id>', methods=['PUT'])
@handle_exceptions
@validate_input(['name'])
def update_director(data, director_id):
    """Updates an existing director."""
    director = update_director_by_id(director_id, data['name'])
    return jsonify({"message": "Director updated successfully", "director": director.to_dict()}), 200


@main.route('/directors/<int:director_id>', methods=['DELETE'])
@handle_exceptions
def delete_director(director_id):
    """Deletes a director and reassigns films to 'unknown'."""
    delete_director_by_id(director_id)
    return success_message("director deleted")


@main.route('/films', methods=['POST'])
@handle_exceptions
@validate_input(['title', 'release_year', 'rating', 'director_id'])
def add_film(data):
    """Adds a new film."""
    film = create_film(data)
    return jsonify(film.to_dict()), 201


@main.route('/films', methods=['GET'])
@handle_exceptions
def get_films():
    """Gets a list of all films."""
    films = get_all_films()
    return jsonify(serialize_objects(films)), 200


@main.route('/films/<int:film_id>', methods=['PUT', 'PATCH'])
@handle_exceptions
def update_film(film_id):
    """Updates an existing film."""
    data = request.get_json()
    film = update_film_by_id(film_id, data)
    return jsonify({"message": "Film updated successfully", "film": film.to_dict()}), 200


@main.route('/films/<int:film_id>', methods=['DELETE'])
@handle_exceptions
def delete_film(film_id):
    """Deletes a film."""
    delete_film_by_id(film_id)
    return success_message("film deleted")
