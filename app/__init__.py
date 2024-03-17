from os import environ
from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager
from app.blueprints.users import users_bp
from app.blueprints.auth import auth_bp
from app.blueprints.posts import posts_bp
from app.blueprints.general import general_bp



def get_settings():
    return environ.get('SETTINGS')

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_settings())

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    _register_blueprints(app)
    
    return app

def _register_blueprints(app):
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(general_bp)
