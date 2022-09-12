from fixtures import db

from .model import Pokemon, Ability


def test_create_a_pokemon(db):
    pokemon = Pokemon(id=1, name='test name')

    db.add(pokemon)
    db.commit()

    first_pokemon = db.query(Pokemon).first()

    assert first_pokemon is not None


def test_create_an_ability(db):
    ability = Ability(id=1, name='test')

    db.add(ability)
    db.commit()

    assert db.query(Ability).first() is not None


def test_create_a_pokemon_with_abilities(db):
    ability1 = Ability(id=1, name='test ability 1')
    ability2 = Ability(id=2, name='test ability 2')
    pokemon = Pokemon(id=1, name='test pokemon')
    pokemon.add_abilities([ability1, ability2])

    db.add(pokemon)
    db.commit()

    pokemon = db.query(Pokemon).first()
    assert pokemon is not None
    assert pokemon.abilities == [ability1, ability2]
