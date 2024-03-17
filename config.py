from os import path, environ


BASE_DIR = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER='app/static/images'


class DevConfig(Config):
    pass


class ProdConfig(Config):
    pass