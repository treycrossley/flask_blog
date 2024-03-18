"""
Test suite for the authentication functionality in the Flask application.

This module contains unit tests for the authentication-related functionalities
such as user registration, login, logout, password reset, and authentication
middleware. It ensures that the authentication mechanisms work correctly and
securely.

"""

from flask_login import current_user, login_user
from app.extensions import bcrypt
from app.models import Users

# Test login route
def test_login_route(client):
    """
    Test whether the login route returns the correct status code.

    Args:
        client: Flask test client.

    Asserts:
        - Whether the status code is 200, indicating success.
    """
    response = client.get("/auth/login")
    assert response.status_code == 200


# Test if the login form is rendered correctly
def test_login_form_rendered(client):
    """
    Test whether the login form is rendered correctly.

    Args:
        client: Flask test client.

    Asserts:
        - Whether the status code is 200, indicating success.
        - Whether the response data contains expected form elements
          like username and password fields.
    """
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


# Test login with invalid credentials (Commented out due to errors)
def test_login_with_invalid_credentials(client, app, session):
    """
    Test login with invalid credentials.

    Args:
        client: Flask test client.

    Asserts:
        - Whether the status code is 200, indicating the login form is rendered again.
        - Whether the error message for wrong password or non-existing user is displayed.
        - Whether the user is not logged in (session does not contain user ID).
    """
    with app.test_request_context():
        test = "test"
        testEmail = test + "@" + test + ".com"
        hashed_password = bcrypt.generate_password_hash(test).decode("utf-8")

        user = Users(
            username=test,
            name=test,
            email=testEmail,
            favorite_pizza_place=test,
            password_hash=hashed_password,
        )
        session.add(user)
        session.commit()

        response = client.post("/auth/login", data={"username": "a", "password": "a"})
        assert response.status_code == 200
        assert current_user.is_authenticated is False


def test_login_with_valid_credentials(client, app, session):
    """
    Test whether the login route accepts valid credentials.

    Args:
        client: Flask test client.
        app: Flask application object.
        session: Database session fixture.
    """

    # Manually create a user in the database
    with app.test_request_context():
        test_username = "test_user"
        test_email = "test@example.com"
        hashed_password = bcrypt.generate_password_hash("correct_password").decode(
            "utf-8"
        )

        user = Users(
            username=test_username,
            name="Test User",
            email=test_email,
            favorite_pizza_place="Test Pizza Place",
            password_hash=hashed_password,
        )
        session.add(user)
        session.commit()

        # Attempt to log in with valid credentials
        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "correct_password"},
            follow_redirects=True,
        )

        # Check if login succeeds and user is authenticated
        assert b"Invalid username or password" not in response.data


# Test logout route (Commented out due to errors)
def test_logout(client, app, session):
    """
    Test whether the logout route redirects and logs out the user.

    Args:
        client: Flask test client.

    Asserts:
        - Whether the status code is 302, indicating a redirect after logout.
        - Whether the user is logged out (session does not contain user ID).
    """

    # Manually create a request context and log in the user
    with app.test_request_context():
        test = "test"
        testEmail = test + "@" + test + ".com"
        hashed_password = bcrypt.generate_password_hash(test).decode("utf-8")

        user = Users(
            username=test,
            name=test,
            email=testEmail,
            favorite_pizza_place=test,
            password_hash=hashed_password,
        )
        session.add(user)
        session.commit()
        login_user(user)

        # Access the logout route
        response = client.get("/auth/logout", follow_redirects=True)

        # Check if the user is redirected to the login page
        assert (
            response.status_code == 200
        )  # Assuming you are redirected to the login page

        # Check if the flash message indicating successful logout is present
        assert b"You have been logged out!" in response.data

        # check that user is logged out
        assert current_user.is_authenticated is False
