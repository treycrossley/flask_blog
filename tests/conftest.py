from unittest.mock import patch
import pytest
from app import create_app, db as _db
from app.models import Users, Posts
from app.forms import LoginForm, PostForm, SearchForm, NamerForm, PasswordForm, UserForm


@pytest.fixture()
def app():
    app = create_app("test")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def init_db(client):
    """Initialize the database."""
    with client.application.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app, init_db):
    """Provide access to the database."""
    return _db


@pytest.fixture
def models(app, db):
    """Fixture to provide access to models."""
    return {"Users": Users, "Posts": Posts}


@pytest.fixture
def forms(app, db):
    """Fixture to provide access to forms."""
    return {
        "LoginForm": LoginForm,
        "PostForm": PostForm,
        "SearchForm": SearchForm,
        "NamerForm": NamerForm,
        "PasswordForm": PasswordForm,
        "UserForm": UserForm,
    }


# Define a fixture to mock the CSRF token
@pytest.fixture
def mock_csrf_token():
    with patch("flask_wtf.csrf.generate_csrf") as generate_csrf_mock:
        generate_csrf_mock.return_value = "mocked_csrf_token"
        yield "mocked_csrf_token"


@pytest.fixture
def authenticated_user(client, db):
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


def authenticated_admin(client, db):
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


@pytest.fixture
def unauthenticated_user(client):
    yield
