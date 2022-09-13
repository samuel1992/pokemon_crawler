from flask import jsonify, Blueprint

from .service import PokemonService

app = Blueprint('pokemon_api', __name__)


@app.route('/pokemons', methods=['GET'])
def get_pokemons():
    return jsonify({
        'pokemons': [p.to_dict() for p in PokemonService().get_all_pokemons()]
    })
