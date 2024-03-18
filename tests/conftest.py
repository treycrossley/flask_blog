import pytest
from app import create_app
from app.extensions import db, bcrypt  # Rename the imported db object
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


# Fixture to create a database session for each test
@pytest.fixture
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()
