from os import environ
from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager, ckEditor
from app.blueprints import auth_bp, posts_bp, general_bp, users_bp
from config import config_by_name





def get_settings():
    return environ.get('SETTINGS')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ckEditor.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    
    _register_blueprints(app)
    
    return app

def _register_blueprints(app):
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(general_bp)
