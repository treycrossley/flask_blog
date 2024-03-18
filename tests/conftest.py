"""
Test fixtures and setup for the Flask application.

This file defines fixtures used in tests across the application. Fixtures are reusable
objects that can be set up before running tests and torn down afterward. They provide
a convenient way to prepare the testing environment and provide access to common resources
such as the Flask application, database session, etc.

Fixtures:
    - app: Fixture to initialize the Flask application and set up the application context.
    - session: Fixture to create a database session for each test.

Usage:
    Fixtures defined in this file are automatically discovered by pytest and made available
    to test functions by simply specifying them as function arguments. For example:

    def test_example(app, session):
        # Use app and session fixtures in the test
"""

import pytest
from app import create_app
from app.extensions import db  # Rename the imported db object


# Fixture to initialize the Flask application
@pytest.fixture
def app():
    """
    Fixture to initialize the Flask application and set up the application context.

    This fixture creates and returns a Flask application configured for testing purposes.
    It sets up the application context so that the application and its extensions are
    properly initialized and ready to be used in tests.

    Returns:
        Flask app: The Flask application object.
    """
    app = create_app("test")
    with app.app_context():
        yield app


# Fixture to create a test client for the Flask application
@pytest.fixture
def client(app):
    """
    Fixture to create a test client for the Flask application.

    This fixture creates a test client for the Flask application provided as input.
    The test client can be used to simulate HTTP requests and interact with the
    application endpoints during testing.

    Args:
        app: Flask application fixture.

    Returns:
        FlaskClient: Test client for the Flask application.
    """
    return app.test_client()


# Fixture to create a database session for each test
@pytest.fixture
def session(app):
    """
    Fixture to create a database session for each test.

    This fixture creates and manages a database session for each test function.
    It sets up the application context, initializes the database, and creates
    a session for database operations. After each test, it rolls back the session
    to maintain a clean state for subsequent tests.

    Args:
        app: Flask application fixture.

    Returns:
        Session: Database session.
    """
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()
