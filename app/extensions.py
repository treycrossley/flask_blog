"""
This module includes the initialization of various Flask extensions required for the application.

- Bcrypt: For password hashing.
- SQLAlchemy: For database ORM.
- Migrate: For database migrations.
- LoginManager: For user session management.
- MetaData: For defining the naming convention for SQLAlchemy.
- CKEditor: For integrating a rich text editor.

The SQLAlchemy MetaData is initialized with a custom naming convention
for database constraints and indexes.
"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_ckeditor import CKEditor

# SQLAlchemy metadata naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Metadata with custom naming convention
metadata = MetaData(naming_convention=convention)

# Initialize Flask extensions
db = SQLAlchemy(metadata=metadata)  # Database ORM
migrate = Migrate(render_as_batch=True)  # Database migrations
bcrypt = Bcrypt()  # Password hashing
login_manager = LoginManager()  # User session management
ckEditor = CKEditor()  # Rich text editor
