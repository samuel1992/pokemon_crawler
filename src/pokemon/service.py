from typing import List

from lib.pokemon_api import PokemonApi

from extensions import db

from .model import Pokemon, Ability
from .schema import PokemonSchema, AbilitySchema


class PokemonService:
    def fetch_new_pokemons(self):
        response = PokemonApi.get_all_pokemons()
        pokemons = [PokemonSchema.from_dict(i).to_instance()
                    for i in response['results']]

        db.session.add_all(pokemons)
        db.session.commit()

    def fetch_new_abilities(self):
        for pokemon in Pokemon.query.all():
            response = PokemonApi.get_pokemon(pokemon.id)
            abilities = [
                AbilitySchema.from_dict(
                    {**{'pokemon_id': pokemon.id}, **a['ability']}
                ).to_instance()
                for a in response['results']
            ]

            db.session.add_all(abilities)
            db.session.commit()
