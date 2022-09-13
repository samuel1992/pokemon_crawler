from flask import Flask, jsonify

from pokemon.api import app as pokemon_app
from pokemon.model import *

from extensions import Base, engine
from config import Config


def create_app():
    flask_app = Flask(__name__)

    Base.metadata.create_all(bind=engine)

    flask_app.config.from_object(Config)

    flask_app.register_blueprint(pokemon_app)

    return flask_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host='0.0.0.0')
