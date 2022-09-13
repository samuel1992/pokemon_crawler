import sqlalchemy

from typing import List
from datetime import datetime

from lib.pokemon_api import PokemonApi

from extensions import db

from .model import Pokemon, Ability
from .schema import PokemonSchema, AbilitySchema


class PokemonService:
    def pokemon_total():
        return db.query(Pokemon).count()

    def ability_total():
        return db.query(Ability).count()

    @staticmethod
    def last_updated_pokemons(amount: int) -> List[int]:
        query = db.query(Pokemon.id).order_by(
            Pokemon.last_update.desc()
        ).limit(amount)
        return [i[0] for i in query.all()]

    @staticmethod
    def fetch_new_pokemons():
        response = PokemonApi.get_all_pokemons()
        pokemons = [PokemonSchema.from_dict(i).to_instance()
                    for i in response['results']]

        for pokemon in pokemons:
            try:
                db.add(pokemon)
                db.commit()
            except sqlalchemy.exc.IntegrityError:
                db.rollback()
            finally:
                db.close()

    @staticmethod
    def fetch_new_abilities(pokemon_id: int):
        pokemon = db.query(Pokemon).get(pokemon_id)
        pokemon.last_update = datetime.now()
        db.add(pokemon)
        db.commit()

        response = PokemonApi.get_pokemon(pokemon.id)

        abilities = []
        for a in response['abilities']:
            ability = AbilitySchema.from_dict(
                {**{'pokemon_id': pokemon.id}, **a['ability']}
            ).to_instance()
            abilities.append(ability)

        for ability in abilities:
            try:
                db.add(ability)
                db.commit()
            except sqlalchemy.exc.IntegrityError:
                db.rollback()
                db.query(Ability).filter(
                    Ability.id == ability.id
                ).update(dict(name=ability.name))
                db.commit()
            finally:
                db.close()
