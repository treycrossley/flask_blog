"""
Module for creating the Flask application instance and registering blueprints and extensions.

This module contains the necessary code to create the Flask application instance, configure it
based on the specified configuration, and register blueprints and extensions.

Functions:
    create_app(config_name): Function to create the Flask application instance based on the
        specified configuration name.

Constants:
    config_by_name: Dictionary containing configurations for different environments.

Imports:
    - Flask: Class for creating the Flask application.
    - config_by_name: Dictionary containing configurations for different environments.
    - auth_bp, posts_bp, general_bp, users_bp: Blueprints for different parts of the application.
    - db, migrate, bcrypt, login_manager, ckEditor: Extensions used in the application.
"""

from os import environ
from flask import Flask
from config import config_by_name
from app.blueprints import auth_bp, posts_bp, general_bp, users_bp
from .extensions import db, migrate, bcrypt, login_manager, ckEditor


def create_app(config_name):
    """
    Creates a Flask application.

    Args:
        config_name (str): The name of the configuration to use.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ckEditor.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    _register_blueprints(app)

    return app


def _register_blueprints(app):
    """
    Registers blueprints with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(general_bp)
