from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from .dto import AbilityDTO, PokemonDTO
from .model import Ability, Pokemon
from .repository import AbilityRepository, IntegrityError, PokemonRepository


def now():
    return datetime.now()


class PokemonRepositoryTest(TestCase):
    def setUp(self):
        self.repository = PokemonRepository(storage=MagicMock(), entity=Pokemon)

    def test_get_by_id(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        self.repository.storage.get_by_id.return_value = pokemon

        assert self.repository.get_by_id(1) == PokemonDTO.from_instance(pokemon)

    def test_get_total(self):
        self.repository.storage.count.return_value = 1

        assert self.repository.get_total() == 1
        self.repository.storage.count.assert_called_with(Pokemon)

    def test_get_all(self):
        pokemons = [
            Pokemon(id=1, name='some name', last_update=now()),
            Pokemon(id=2, name='another name', last_update=now()),
            Pokemon(id=3, name='one more name', last_update=now())
        ]
        self.repository.storage.get_all.return_value = pokemons

        assert (
            self.repository.get_all(2) ==
            [PokemonDTO.from_instance(i) for i in pokemons]
        )
        self.repository.storage.get_all.assert_called_with(Pokemon, 2)

    def test_create(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.get_by_id.return_value = pokemon

        assert pokemon_dto == self.repository.create(pokemon_dto)

    def test_update(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.get_by_id.return_value = pokemon_dto

        assert pokemon_dto == self.repository.update(pokemon_dto)

    def test_try_to_create_duplicate(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.create.side_effect = IntegrityError()

        with pytest.raises(IntegrityError):
            assert pokemon_dto == self.repository.create(pokemon_dto)


class AbilityRepositoryTest(TestCase):
    def setUp(self):
        self.repository = AbilityRepository(storage=MagicMock(), entity=Ability)

    def test_get_total(self):
        self.repository.storage.count.return_value = 1

        assert self.repository.get_total() == 1
        self.repository.storage.count.assert_called_with(Ability)

    def test_create(self):
        ability = Ability(id=1, name='test ability 1')
        ability_dto = AbilityDTO.from_instance(ability)
        self.repository.storage.get_by_id.return_value = ability

        assert ability_dto == self.repository.create(ability_dto)

    def test_update(self):
        ability = Ability(id=1, name='test ability 1')
        ability_dto = AbilityDTO.from_instance(ability)
        self.repository.storage.get_by_id.return_value = ability_dto

        assert ability_dto == self.repository.update(ability_dto)

    def test_try_to_create_duplicate(self):
        ability = Ability(id=1, name='test ability 1')
        ability_dto = AbilityDTO.from_instance(ability)
        self.repository.storage.create.side_effect = IntegrityError()

        with pytest.raises(IntegrityError):
            assert ability_dto == self.repository.create(ability_dto)
