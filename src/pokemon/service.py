import sqlalchemy

from typing import List
from datetime import datetime

from lib.pokemon_api import PokemonApi

from extensions import db

from .model import Pokemon, Ability
from .dto import PokemonDTO, AbilityDTO


class PokemonService:
    def __init__(self, db_session=None):
        self._db = db_session or db

    def pokemon_total(self):
        return self._db.query(Pokemon).count()

    def ability_total(self):
        return self._db.query(Ability).count()

    def last_updated_pokemons(self, amount: int) -> List[int]:
        query = self._db.query(Pokemon.id).order_by(
            Pokemon.last_update.desc()
        ).limit(amount)
        return [i[0] for i in query.all()]

    def fetch_new_pokemons(self):
        response = PokemonApi.get_all_pokemons()
        pokemons = [PokemonDTO.from_dict(i).to_instance()
                    for i in response]

        for pokemon in pokemons:
            try:
                self._db.add(pokemon)
                self._db.commit()
            except sqlalchemy.exc.IntegrityError:
                self._db.rollback()
            finally:
                self._db.close()

    def fetch_new_abilities(self, pokemon_id: int):
        pokemon = self._db.query(Pokemon).get(pokemon_id)
        pokemon.last_update = datetime.now()
        self._db.add(pokemon)
        self._db.commit()

        response = PokemonApi.get_pokemon(pokemon.id)

        abilities = []
        for a in response['abilities']:
            ability = AbilityDTO.from_dict(
                {**{'pokemon_id': pokemon.id}, **a['ability']}
            ).to_instance()
            abilities.append(ability)

        for ability in abilities:
            try:
                self._db.add(ability)
                self._db.commit()
            except sqlalchemy.exc.IntegrityError:
                self._db.rollback()
                self._db.query(Ability).filter(
                    Ability.id == ability.id
                ).update(dict(name=ability.name))
                self._db.commit()
            finally:
                self._db.close()

    def get_all_pokemons(self):
        return [PokemonDTO.from_instance(i)
                for i in self._db.query(Pokemon).all()]
