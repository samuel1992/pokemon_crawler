from fixtures import db

from .model import Pokemon, Ability


def test_create_a_pokemon(db):
    pokemon = Pokemon(id=1, name='test name')

    db.session.add(pokemon)
    db.session.commit()

    first_pokemon = Pokemon.query.first()

    assert first_pokemon is not None


def test_add_pokemon_description(db):
    pokemon = Pokemon(id=1, name='test name')
    pokemon.add_description(height=1, weight=1, species_name='test specie')

    db.session.add(pokemon)
    db.session.commit()

    first_pokemon = Pokemon.query.first()

    assert first_pokemon is not None

    assert first_pokemon.description == (
        'This pokemon has height: 1, weight: 1 and belongs to test specie'
    )


def test_edit_pokemon_description_after_query(db):
    pokemon = Pokemon(id=1, name='test name')

    db.session.add(pokemon)
    db.session.commit()

    first_pokemon = Pokemon.query.first()
    first_pokemon.add_description(
        height=1, weight=1, species_name='test specie'
    )

    assert first_pokemon is not None

    assert first_pokemon.description == (
        'This pokemon has height: 1, weight: 1 and belongs to test specie'
    )
