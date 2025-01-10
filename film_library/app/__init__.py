from flask import Flask
from app.extensions import db, migrate, login_manager
from app.models import Film, Director
from app.routes import main
from app.auth import auth
from app.config import Config
from app.database import seed_database

def create_app(config_class=Config):
    """
    Создает экземпляр приложения Flask с заданной конфигурацией.

    :param config_class: Класс конфигурации для приложения.
    :return: Настроенное приложение Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация маршрутов
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    # Инициализация базы данных
    with app.app_context():
        db.create_all()
        seed_database()  # Инициализация начальных данных

    return app
