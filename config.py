from os import path, environ


BASE_DIR = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER='app/static/images' 

class DevConfig(Config):
    DEBUG=True
    pass


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_blog.db'
    TESTING=True
    WTF_CSRF_ENABLED = True

    pass


config_by_name = dict(
    dev=DevConfig,
    test=TestConfig
)