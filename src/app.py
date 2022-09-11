from flask import Flask

from extensions import db


def create_app():
    flask_app = Flask(__name__)

    db.init_app(flask_app)

    return flask_app
