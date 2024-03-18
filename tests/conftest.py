import pytest
from app import create_app, db as _db
from app.models import Users, Posts
from os import environ

def get_settings():
    return environ.get('SETTINGS')

@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object(get_settings())
    app.config['TESTING'] = True
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """Initialize the database."""
    _db.app = app
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def models(app, db):
    """Fixture to provide access to models."""
    return {'Users': Users, 'Posts': Posts}