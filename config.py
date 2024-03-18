from os import path


class Config:
    """Base configuration class."""

    SECRET_KEY = "1234"
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "app/static/images"


class DevConfig(Config):
    """Development configuration class."""

    DEBUG = True


class TestConfig(Config):
    """Test configuration class."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///test_blog.db"
    TESTING = True
    WTF_CSRF_ENABLED = True


config_by_name = dict(dev=DevConfig, test=TestConfig)
