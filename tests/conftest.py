from unittest.mock import patch
import pytest
from app import create_app, db as _db
from app.models import Users, Posts
from app.forms import LoginForm, PostForm, SearchForm, NamerForm, PasswordForm, UserForm


# Fixture to create the Flask application for testing
@pytest.fixture()
def app():
    """Create a Flask application instance for testing."""
    app = create_app("test")
    yield app


# Fixture to provide a test client for making requests to the Flask application
@pytest.fixture()
def client(app):
    """Provide a test client for making requests to the Flask application."""
    return app.test_client()


# Fixture to initialize the database before each test
@pytest.fixture
def init_db(client):
    """Initialize the database before each test."""
    with client.application.app_context():
        _db.create_all()
        yield _db
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


# Fixture to mock the generation of CSRF tokens
@pytest.fixture
def mock_csrf_token():
    """Fixture to mock the generation of CSRF tokens."""
    with patch("flask_wtf.csrf.generate_csrf") as generate_csrf_mock:
        generate_csrf_mock.return_value = "mocked_csrf_token"
        yield "mocked_csrf_token"


# Fixture to create and authenticate a regular user for testing
@pytest.fixture
def authenticated_user(client, db):
    """Fixture to create and authenticate a regular user for testing."""
    # Create a test user in the database
    user = Users(username="test_user", name="Test User", email="test@example.com")
    user.set_password("password")  # Set a password for the user
    db.session.add(user)
    db.session.commit()

    # Log in the user
    with client.session_transaction() as session:
        session["_user_id"] = user.id

    yield user  # Provide the user object to the test function

    # Clean up: Log out the user after the test
    with client.session_transaction() as session:
        session.pop("_user_id", None)


# Fixture to create and authenticate an admin user for testing
@pytest.fixture
def authenticated_admin(client, db):
    """Fixture to create and authenticate an admin user for testing."""
    # Create a test admin user in the database
    admin_user = Users(
        username="admin_user",
        name="Admin User",
        email="admin@example.com",
        is_admin=True,
    )
    admin_user.set_password("admin_password")  # Set a password for the admin user
    db.session.add(admin_user)
    db.session.commit()

    # Log in the admin user
    with client.session_transaction() as session:
        session["_user_id"] = admin_user.id

    yield admin_user  # Provide the admin user object to the test function

    # Clean up: Log out the admin user after the test
    with client.session_transaction() as session:
        session.pop("_user_id", None)


# Fixture for an unauthenticated user
@pytest.fixture
def unauthenticated_user(client):
    """Fixture for an unauthenticated user."""
    yield
