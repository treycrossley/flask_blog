from os import environ
from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager, ckEditor
from app.blueprints import auth_bp, posts_bp, general_bp, users_bp





def get_settings():
    return environ.get('SETTINGS')

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_settings())

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ckEditor.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        db.create_all()
    
    
    _register_blueprints(app)
    
    return app

def _register_blueprints(app):
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(general_bp)
