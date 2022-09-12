from fixtures import db, app

from .model import Pokemon, Ability


def test_create_a_pokemon(db):
    pokemon = Pokemon(id=1, name='test name')

    db.session.add(pokemon)
    db.session.commit()

    first_pokemon = Pokemon.query.first()

    assert first_pokemon is not None


def test_create_an_ability(db):
    ability = Ability(id=1, name='test')

    db.session.add(ability)
    db.session.commit()

    assert Ability.query.first() is not None


def test_an_pokemon_with_abilities(db):
    ability1 = Ability(id=1, name='test ability 1')
    ability2 = Ability(id=2, name='test ability 2')
    pokemon = Pokemon(id=1, name='test pokemon')
    pokemon.add_abilities([ability1, ability2])

    db.session.add(pokemon)
    db.session.commit()

    pokemon = Pokemon.query.first()
    assert pokemon is not None
    assert pokemon.abilities == [ability1, ability2]
