from flask import Flask

from extensions import db, Base, engine
from config import Config


def create_app():
    flask_app = Flask(__name__)

    Base.metadata.create_all(bind=engine)

    flask_app.config.from_object(Config)

    return flask_app
