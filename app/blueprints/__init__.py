"""
Module docstring for blueprint imports.

This module imports blueprints for different parts of the application.

Attributes:
    auth_bp: Blueprint object for authentication-related routes.
    general_bp: Blueprint object for general routes.
    posts_bp: Blueprint object for post-related routes.
    users_bp: Blueprint object for user-related routes.
"""

from .auth import auth_bp
from .general import general_bp
from .posts import posts_bp
from .users import users_bp
