import os

from extensions import Base, engine
from pokemon.model import Ability, Pokemon
from pokemon.service import PokemonService


def get_new_abilities(pokemon_id: int):
    service = PokemonService()
    service.fetch_new_abilities(pokemon_id)

    print(f'Total abilities in db: {service.ability_total()}')


def get_new_pokemons():
    service = PokemonService()
    service.fetch_new_pokemons()

    print(f'Total pokemons in db: {service.pokemon_total()}')

    # for pokemon_id in service.last_updated_pokemons(10):
    #    get_new_abilities.delay(pokemon_id)


get_new_pokemons()
