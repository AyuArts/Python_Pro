from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Реєстрація нового користувача."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "Користувач з таким іменем або email вже існує"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Користувача зареєстровано успішно"}), 201


@auth.route('/login', methods=['POST'])
def login():
    """Вхід користувача."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Вхід виконано успішно"}), 200
    return jsonify({"error": "Неправильний email або пароль"}), 401


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """Вихід користувача."""
    logout_user()
    return jsonify({"message": "Ви вийшли"}), 200
