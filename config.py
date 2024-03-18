"""
Configuration Classes

Defines configuration classes for different environments: base configuration,
development configuration, and test configuration.

Attributes:
    - Config: Base configuration class with common settings such as secret key,
      database URI, track modifications, and upload folder.
    - DevConfig: Development configuration class inheriting from Config,
      enabling debug mode.
    - TestConfig: Test configuration class inheriting from Config, configuring
      the database URI for testing and enabling testing mode with CSRF protection.

    - config_by_name: Dictionary mapping environment names to their respective
      configuration classes for easy access and configuration loading.

"""

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
