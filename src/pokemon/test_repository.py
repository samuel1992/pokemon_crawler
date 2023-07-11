from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from .dto import AbilityDTO, PokemonDTO
from .model import Ability, Pokemon
from .repository import AbilityRepository, PokemonRepository


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
            self.repository.get_all(2)
            == [PokemonDTO.from_instance(i) for i in pokemons]
        )
        self.repository.storage.get_all.assert_called_with(Pokemon, 2)

    def test_create(self):
        pokemon = Pokemon(id=1, name='some name', last_update=now())
        pokemon_dto = PokemonDTO.from_instance(pokemon)
        self.repository.storage.get_by_id.return_value = pokemon

        assert pokemon_dto == self.repository.create(pokemon_dto)

class AbilityRepositoryTest(TestCase):
    def setUp(self):
        self.repository = AbilityRepository(storage=MagicMock(), entity=Ability)

    def test_get_total(self):
        self.repository.storage.count.return_value = 1

        assert self.repository.get_total() == 1
        self.repository.storage.count.assert_called_with(Ability)
