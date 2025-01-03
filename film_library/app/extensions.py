from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Будь ласка, увійдіть, щоб отримати доступ."

db = SQLAlchemy()
migrate = Migrate()