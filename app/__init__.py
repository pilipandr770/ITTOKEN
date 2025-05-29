# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # Підключення blueprint'ів
    from app.main.routes import main
    from app.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    return app

from app.models import User

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Повертає користувача для Flask-Login за id"""
    return User.query.get(int(user_id))
