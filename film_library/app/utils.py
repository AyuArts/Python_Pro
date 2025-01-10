from flask import request, jsonify
from functools import wraps


def validate_input(required_fields):
    """Decorator to validate input data against required fields."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            missing = [field for field in required_fields if field not in data or not data[field]]
            if missing:
                return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
            return func(data, *args, **kwargs)
        return wrapper
    return decorator


def handle_exceptions(func):
    """Decorator for handling exceptions in routes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper


def serialize_objects(objects):
    """Serializes a list of objects using their `to_dict` method."""
    return [obj.to_dict() for obj in objects]


def success_message(action):
    """Generates a standardized success message."""
    return jsonify({"message": f"{action.capitalize()} successfully"}), 200
