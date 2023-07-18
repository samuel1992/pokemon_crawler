from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from fixtures import db
from lib.immudb_api import ImmuDBClient

from .dto import AbilityDTO, PokemonDTO
from .model import Ability, Pokemon
from .storage import ImmuDBStorage, PostgresStorage


class TestPostgresStorage:
    def test_create_a_pokemon(self, db):
        storage = PostgresStorage(db_engine=db)
        now = datetime.now()
        pokemon = PokemonDTO(id=1, name='test name', last_update=now)

        storage.create(pokemon)

        first_pokemon = db.query(Pokemon).first()

        assert first_pokemon is not None
        assert isinstance(first_pokemon, Pokemon)

    def test_create_a_duplicated_pokemon(self, db):
        storage = PostgresStorage(db_engine=db)
        now = datetime.now()
        pokemon = PokemonDTO(id=1, name='new pokemon', last_update=now)

        storage.create(pokemon)

        first_pokemon = db.query(Pokemon).first()

        assert first_pokemon is not None
        assert isinstance(first_pokemon, Pokemon)

        duplicated_pokemon = PokemonDTO(id=1, name='new pokemon with used id', last_update=now)

        assert storage.create(duplicated_pokemon) is None

    def test_update_a_pokemon(self, db):
        initial_name = 'test pokemon'
        initial_update = datetime.now()
        storage = PostgresStorage(db_engine=db)
        pokemon = Pokemon(id=1, name=initial_name, last_update=initial_update)

        db.add(pokemon)
        db.commit()

        first_pokemon = db.query(Pokemon).first()
        assert first_pokemon is not None

        pokemon = PokemonDTO(id=1, name='New pokemon name', last_update=datetime.now())
        storage.update(pokemon)

        first_pokemon = db.query(Pokemon).first()
        assert first_pokemon.name != initial_name
        assert first_pokemon.last_update != initial_update

    def test_get_all_pokemons(self, db):
        now = datetime.now()
        pokemon1 = Pokemon(id=1, name='some name', last_update=now)
        pokemon2 = Pokemon(id=2, name='another name', last_update=now)

        db.add(pokemon1)
        db.add(pokemon2)
        db.commit()

        storage = PostgresStorage(db_engine=db)

        pokemons = storage.get_all(PokemonDTO)

        assert len(pokemons) == 2

    def test_get_all_pokemons_with_limit(self, db):
        now = datetime.now()
        for i in range(20):
            pokemon = Pokemon(id=i, name=f'some name {i}', last_update=now)
            db.add(pokemon)

        db.commit()

        storage = PostgresStorage(db_engine=db)

        pokemons = storage.get_all(PokemonDTO, limit=10)

        assert len(pokemons) == 10

    def test_count_pokemons(self, db):
        now = datetime.now()
        for i in range(10):
            pokemon = Pokemon(id=i, name=f'some name {i}', last_update=now)
            db.add(pokemon)

        db.commit()

        storage = PostgresStorage(db_engine=db)

        assert storage.count(PokemonDTO) == 10

    def test_get_pokemon_by_id(self, db):
        storage = PostgresStorage(db_engine=db)
        pokemon = Pokemon(id=1, name='some name', last_update=datetime.now())

        db.add(pokemon)
        db.commit()

        assert storage.get_by(PokemonDTO, 'id', 1)

    def test_get_ability_by_name(self, db):
        storage = PostgresStorage(db_engine=db)
        ability = Ability(id=1, name='test')

        db.add(ability)
        db.commit()

        result = storage.get_by(AbilityDTO, 'name', 'test')

        assert result is not None
        assert result.name == 'test'

        result = storage.get_by(AbilityDTO, 'name', 'nonexistent')
        assert result is None


class ImmuDBStorageTest(TestCase):
    def setUp(self):
        self.client_mock = MagicMock(spec=ImmuDBClient)
        self.storage = ImmuDBStorage(immudb_client=self.client_mock)

    def test_create(self):
        dto_mock = MagicMock()
        dto_mock.to_dict.return_value = {'key': 'value'}
        document_mock = MagicMock(id='document_id')
        self.client_mock.create_document.return_value = document_mock

        result = self.storage.create(dto_mock)

        self.assertEqual(result, 'document_id')
        self.client_mock.create_document.assert_called_with({'key': 'value'})

    def test_get_by(self):
        dto_mock = MagicMock()
        data = {
            "id": "1",
            "last_update": "2023-23-18 09:23:14",
            "name": "bulbasaur"
        }
        result_mock = MagicMock(data=data)
        self.client_mock.search.return_value = [result_mock]

        self.storage.get_by(dto_mock, 'id', '1')

        dto_mock.assert_called()

    def test_get_all(self):
        dto_mock = MagicMock()
        data = {
            "id": "1",
            "last_update": "2023-23-18 09:23:14",
            "name": "bulbasaur"
        }
        result_mock = MagicMock(data=data)
        self.client_mock.search.return_value = [result_mock]

        result = self.storage.get_all(dto_mock)

        self.client_mock.search.assert_called()

    def test_update(self):
        dto_mock = MagicMock(id='document_id')
        dto_mock.to_dict.return_value = {'key': 'value'}
        document_mock = MagicMock(id='updated_document_id')
        self.client_mock.update_document.return_value = document_mock

        result = self.storage.update(dto_mock, {'new_key': 'new_value'})

        self.assertEqual(result, 'updated_document_id')
        self.client_mock.update_document.assert_called()

    def test_count(self):
        self.client_mock.count.return_value = 5

        result = self.storage.count()

        self.assertEqual(result, 5)
        self.client_mock.count.assert_called()
