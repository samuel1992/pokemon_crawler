import pytest

from datetime import datetime

from fixtures import db

from .model import Pokemon, Ability
from .storage import PostgresStorage


def test_create_a_pokemon(db):
    storage = PostgresStorage(db_engine=db)
    now = datetime.now()
    pokemon = Pokemon(id=1, name='test name', last_update=now)

    storage.create(pokemon)

    first_pokemon = db.query(Pokemon).first()

    assert first_pokemon is not None
    assert isinstance(first_pokemon, Pokemon)


def test_create_a_duplicated_pokemon(db):
    storage = PostgresStorage(db_engine=db)
    now = datetime.now()
    pokemon = Pokemon(id=1, name='new pokemon', last_update=now)

    storage.create(pokemon)

    first_pokemon = db.query(Pokemon).first()

    assert first_pokemon is not None
    assert isinstance(first_pokemon, Pokemon)

    duplicated_pokemon = Pokemon(id=1, name='new pokemon with used id', last_update=now)

    assert storage.create(duplicated_pokemon) is None


def test_update_a_pokemon(db):
    initial_name = 'test pokemon'
    initial_update = datetime.now()
    storage = PostgresStorage(db_engine=db)
    pokemon = Pokemon(id=1, name=initial_name, last_update=initial_update)

    db.add(pokemon)
    db.commit()

    first_pokemon = db.query(Pokemon).first()
    assert first_pokemon is not None

    pokemon = Pokemon(id=1, name='New pokemon name', last_update=datetime.now())
    storage.update(pokemon)

    first_pokemon = db.query(Pokemon).first()
    assert first_pokemon.name != initial_name
    assert first_pokemon.last_update != initial_update


def test_get_all_pokemons(db):
    now = datetime.now()
    pokemon1 = Pokemon(id=1, name='some name', last_update=now)
    pokemon2 = Pokemon(id=2, name='another name', last_update=now)

    db.add(pokemon1)
    db.add(pokemon2)
    db.commit()

    storage = PostgresStorage(db_engine=db)

    pokemons = storage.get_all(Pokemon)

    assert len(pokemons) == 2


def test_get_all_pokemons_with_limit(db):
    now = datetime.now()
    for i in range(20):
        pokemon = Pokemon(id=i, name=f'some name {i}', last_update=now)
        db.add(pokemon)

    db.commit()

    storage = PostgresStorage(db_engine=db)

    pokemons = storage.get_all(Pokemon, limit=10)

    assert len(pokemons) == 10


def test_count_pokemons(db):
    now = datetime.now()
    for i in range(10):
        pokemon = Pokemon(id=i, name=f'some name {i}', last_update=now)
        db.add(pokemon)

    db.commit()

    storage = PostgresStorage(db_engine=db)

    assert storage.count(Pokemon) == 10


def test_get_pokemon_by_id(db):
    storage = PostgresStorage(db_engine=db)
    pokemon = Pokemon(id=1, name='some name', last_update=datetime.now())

    db.add(pokemon)
    db.commit()

    assert pokemon == storage.get_by_id(Pokemon, 1)


def test_get_ability_by_name(db):
    storage = PostgresStorage(db_engine=db)
    ability = Ability(id=1, name='test')

    db.add(ability)
    db.commit()

    result = storage.get_by(Ability, 'name', 'test')

    assert result is not None
    assert result.name == 'test'

    result = storage.get_by(Ability, 'name', 'nonexistent')
    assert result is None
