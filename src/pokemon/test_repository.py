from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from .dto import AbilityDTO, PokemonDTO
from .model import Ability, Pokemon
from .repository import Repository


def now():
    return datetime.now()


class PokemonRepositoryTest(TestCase):
    def setUp(self):
        self.repository = Repository(storage=MagicMock(), dto_class=PokemonDTO)

    def test_get_by_id(self):
        pokemon = PokemonDTO(id=1, name='some name', last_update=now())
        self.repository.storage.get_by.return_value = pokemon

        assert self.repository.get_by_id(1) == PokemonDTO.from_instance(pokemon)

    def test_get_total(self):
        self.repository.storage.count.return_value = 1

        assert self.repository.get_total() == 1
        self.repository.storage.count.assert_called_with(PokemonDTO)

    def test_get_all(self):
        pokemons = [
            PokemonDTO(id=1, name='some name', last_update=now()),
            PokemonDTO(id=2, name='another name', last_update=now()),
            PokemonDTO(id=3, name='one more name', last_update=now())
        ]
        self.repository.storage.get_all.return_value = pokemons

        assert (
            self.repository.get_all(2) ==
            [PokemonDTO.from_instance(i) for i in pokemons]
        )
        self.repository.storage.get_all.assert_called_with(PokemonDTO, 2)

    def test_create(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.get_by.return_value = pokemon_dto

        assert pokemon_dto == self.repository.create(pokemon_dto)

    def test_update(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.get_by.return_value = pokemon_dto

        assert pokemon_dto == self.repository.update(pokemon_dto)
        self.repository.storage.update.assert_called()


class AbilityRepositoryTest(TestCase):
    def setUp(self):
        self.repository = Repository(storage=MagicMock(), dto_class=AbilityDTO)

    def test_get_total(self):
        self.repository.storage.count.return_value = 1

        assert self.repository.get_total() == 1
        self.repository.storage.count.assert_called_with(AbilityDTO)

    def test_create(self):
        ability = Ability(id=1, name='test ability 1')
        ability_dto = AbilityDTO.from_instance(ability)
        self.repository.storage.get_by.return_value = ability_dto

        assert ability_dto == self.repository.create(ability_dto)

    def test_update(self):
        ability = Ability(id=1, name='test ability 1')
        ability_dto = AbilityDTO.from_instance(ability)
        self.repository.storage.get_by.return_value = ability_dto

        assert ability_dto == self.repository.update(ability_dto)
        self.repository.storage.update.assert_called()

    def test_get_by_name(self):
        ability = AbilityDTO(id=1, name='test')
        self.repository.storage.get_by.return_value = ability

        result = self.repository.get_by_name('test')

        assert result == ability
        self.repository.storage.get_by.assert_called_with(AbilityDTO, 'name', 'test')
