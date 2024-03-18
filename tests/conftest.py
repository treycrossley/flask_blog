import pytest
from app import create_app
from app.extensions import db as _db  # Rename the imported db object
from app.models import Users, Posts
from app.forms import LoginForm, PasswordForm, NamerForm, PostForm, SearchForm, UserForm


# Fixture to initialize the Flask application
@pytest.fixture
def app():
    app = create_app("test")
    with app.app_context():
        yield app


# Fixture to create a test client for the Flask application
@pytest.fixture
def client(app):
    return app.test_client()


# Fixture to initialize the database before testing
@pytest.fixture
def init_db(app):
    with app.app_context():
        _db.create_all()
        # Optionally, add any necessary test data

        yield  # This is where the testing happens

        _db.session.remove()
        _db.drop_all()


# Fixture to provide access to the database for tests
@pytest.fixture
def db(app, init_db):
    """Provide access to the database for tests."""
    return _db


# Fixture to provide access to model classes for tests
@pytest.fixture
def models(app, db):
    """Fixture to provide access to model classes for tests."""
    return {"Users": Users, "Posts": Posts}


# Fixture to provide access to form classes for tests
@pytest.fixture
def forms(app, db):
    """Fixture to provide access to form classes for tests."""
    return {
        "LoginForm": LoginForm,
        "PostForm": PostForm,
        "SearchForm": SearchForm,
        "NamerForm": NamerForm,
        "PasswordForm": PasswordForm,
        "UserForm": UserForm,
    }
