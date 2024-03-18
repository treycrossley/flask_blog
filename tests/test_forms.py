import pytest
from flask_wtf.csrf import generate_csrf
from app.forms import LoginForm, PostForm, SearchForm, NamerForm, PasswordForm, UserForm


def test_login_form_validation(app):
    """
    Test the validation of the login form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context(
        "/auth/login",
        method="POST",
        data={"username": "valid_username", "password": "valid_password"},
    ):
        form = LoginForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing username
        form.username.data = ""
        form.password.data = "valid_password"
        assert not form.validate()

        # Test missing password
        form.username.data = "valid_username"
        form.password.data = ""
        assert not form.validate()


# Test for PostForm
def test_post_form_validation(app):
    """
    Test the validation of the post form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context(
        "/submit_post",
        method="POST",
        data={
            "title": "Test Post",
            "content": "This is a test post.",
            "author": "Test Author",
            "slug": "test-post",
        },
    ):
        form = PostForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing title
        form.title.data = ""
        assert not form.validate()

        # Test missing content
        form.title.data = "Test Post"
        form.content.data = ""
        assert not form.validate()

        # Test missing slug
        form.content.data = "This is a test post."
        form.slug.data = ""
        assert not form.validate()


# Test for SearchForm
def test_search_form_validation(app):
    """
    Test the validation of the search form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context(
        "/search", method="POST", data={"searched": "keyword"}
    ):
        form = SearchForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing searched term
        form.searched.data = ""
        assert not form.validate()


# Test for NamerForm
def test_namer_form_validation(app):
    """
    Test the validation of the namer form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context("/get_name", method="POST", data={"name": "John"}):
        form = NamerForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing name
        form.name.data = ""
        assert not form.validate()


# Test for PasswordForm
def test_password_form_validation(app):
    """
    Test the validation of the password form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context(
        "/register", method="POST", data={"email": "test@example.com", "pw": "password"}
    ):
        form = PasswordForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing email
        form.email.data = ""
        assert not form.validate()

        # Test missing password
        form.email.data = "test@example.com"
        form.pw.data = ""
        assert not form.validate()


# Test for UserForm
def test_user_form_validation(app):
    """
    Test the validation of the user form.

    Args:
        app: Flask application instance.
        forms: Fixture providing access to form classes.

    """
    with app.test_request_context(
        "/register_user",
        method="POST",
        data={
            "name": "Test User",
            "username": "test_user",
            "email": "test@example.com",
            "favorite_pizza_place": "Pizza Hut",
            "password": "password",
            "password2": "password",
        },
    ):
        form = UserForm()
        form.csrf_token.data = generate_csrf()

        # Test valid data
        assert form.validate()

        # Test missing name
        form.name.data = ""
        assert not form.validate()

        # Test missing username
        form.name.data = "Test User"
        form.username.data = ""
        assert not form.validate()

        # Test missing email
        form.username.data = "test_user"
        form.email.data = ""
        assert not form.validate()

        # Test missing password
        form.email.data = "test@example.com"
        form.password.data = ""
        assert not form.validate()

        # Test passwords mismatch
        form.password.data = "password"
        form.password2.data = "different_password"
        assert not form.validate()
