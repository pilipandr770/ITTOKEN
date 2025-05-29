# app/__init__.py
from flask import Flask, g, request, session
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

    # Зберігати вибір мови в сесії
    @app.before_request
    def set_lang():
        lang = request.args.get('lang')
        if lang:
            session['lang'] = lang
        g.lang = session.get('lang', None)

    # Підключення blueprint'ів
    from app.main.routes import main
    from app.admin.routes import admin
    from .assist import assist_bp
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(assist_bp)

    return app

# Babel локалізатор
@babel.localeselector
def get_locale():
    from flask import request, session
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
        return lang
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(['uk', 'en', 'de', 'ru'])

from app.models import User

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Повертає користувача для Flask-Login за id"""
    return User.query.get(int(user_id))
