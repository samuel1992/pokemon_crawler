from datetime import datetime

from fixtures import db

from .model import Ability, Pokemon
from .storage import PostgresStorage


def test_create_a_pokemon(db):
    storage = PostgresStorage(db_engine=db)
    now = datetime.now()
    pokemon = Pokemon(id=1, name='test name', last_update=now)

    storage.create(pokemon)

    first_pokemon = db.query(Pokemon).first()

    assert first_pokemon is not None
    assert first_pokemon.last_update == now


def test_create_an_ability(db):
    storage = PostgresStorage(db_engine=db)
    ability = Ability(id=1, name='test')

    storage.create(ability)

    assert db.query(Ability).first() is not None


def test_update_a_pokemon(db):
    initial_name = 'test pokemon'
    initial_update = datetime.now()
    storage = PostgresStorage(db_engine=db)
    pokemon = Pokemon(id=1, name=initial_name, last_update=initial_update)

    db.add(pokemon)
    db.commit()

    first_pokemon = db.query(Pokemon).first()
    assert first_pokemon is not None

    storage.update(
        Pokemon, dict(id=1, name='New pokemon name', last_update=datetime.now())
    )

    first_pokemon = db.query(Pokemon).first()
    assert first_pokemon.name != initial_name
    assert first_pokemon.last_update != initial_update


def test_update_an_ability(db):
    initial_name = 'test ability'
    storage = PostgresStorage(db_engine=db)
    ability = Ability(id=1, name=initial_name)

    db.add(ability)
    db.commit()

    first_ability = db.query(Ability).first() is not None
    assert first_ability is not None

    storage.update(
        Ability, dict(id=1, name='New ability name')
    )

    first_ability = db.query(Ability).first()
    assert first_ability.name != initial_name


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
