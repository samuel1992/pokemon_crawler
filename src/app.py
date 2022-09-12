from flask import Flask

from extensions import db
from config import Config, TestingConfig


def create_app(testing=False):
    flask_app = Flask(__name__)

    if testing:
        flask_app.config.from_object(TestingConfig)
    else:
        flask_app.config.from_object(Config)

    db.init_app(flask_app)

    return flask_app
