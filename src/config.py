import os


class Config():
    DEBUG = True
    DATABASE_NAME = os.environ.get('DB_NAME')
    DATABASE_USER = os.environ.get('DB_USER')
    DATABASE_HOST = os.environ.get('DB_HOST')
    DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
    PORT = '8080'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath(os.path.dirname(__file__))}/app-test.db'
