from datetime import datetime
from typing import List, Optional

import sqlalchemy

from extensions import db
from lib.pokemon_api import PokemonApi

from .dto import AbilityDTO, PokemonDTO
from .model import Ability, Pokemon
from .repository import AbilityRepository, PokemonRepository
from .storage import PostgresStorage


class PokemonService:
    def __init__(
        self,
        pokemon_repository: Optional[PokemonRepository] = None,
        ability_repository: Optional[AbilityRepository] = None
    ):
        self.pokemon_repository = pokemon_repository or PokemonRepository(
            storage=PostgresStorage(),
            entity=Pokemon
        )
        self.ability_repository = ability_repository or AbilityRepository(
            storage=PostgresStorage(),
            entity=Ability
        )

    def get_all_pokemons(self) -> List[PokemonDTO]:
        return [PokemonDTO.from_instance(i) for i in self.pokemon_repository.get_all()]

    def pokemon_total(self):
        return self.pokemon_repository.get_total()

    def ability_total(self):
        return self.ability_repository.get_total()

    def last_updated_pokemons(self, amount: int) -> List[Optional[int]]:
        result = self.pokemon_repository.get_all(amount)
        if len(result) < 1:
            return []

        return [i.id for i in result]

    def fetch_new_pokemons(self):
        response = PokemonApi.get_all_pokemons()
        pokemons = [PokemonDTO.from_dict(i) for i in response]
        for pokemon in pokemons:
            found = self.pokemon_repository.get_by_id(pokemon.id)
            if found is None:
                self.pokemon_repository.create(pokemon)

    def fetch_new_abilities(self, pokemon_id: int):
        pokemon_dto = self.pokemon_repository.get_by_id(pokemon_id)
        pokemon_dto.last_update = datetime.now()
        self.pokemon_repository.update(pokemon_dto)

        response = PokemonApi.get_pokemon(pokemon_dto.id)

        abilities = []
        for a in response['abilities']:
            abilities.append(AbilityDTO.from_dict(
                {**{'pokemon_id': pokemon_dto.id}, **a['ability']}
            ))

        for ability_dto in abilities:
            found = self.ability_repository.get_by_name(ability_dto.name)
            if found is None:
                self.ability_repository.create(ability_dto)
            else:
                self.ability_repository.update(ability_dto)
