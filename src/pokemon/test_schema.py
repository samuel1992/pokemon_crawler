from .schema import AbilitySchema, PokemonSchema
from .model import Pokemon, Ability

from fixtures import db


def teste_create_a_ability_schema():
    ability_schema = AbilitySchema(id=1, name='test')

    assert ability_schema.to_dict() == {
        'id': 1,
        'name': 'test',
        'pokemon_id': None
    }


def test_create_a_pokemon_schema():
    pokemon_schema = PokemonSchema(
        id=1, name='test', description='test description'
    )

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test',
        'description': 'test description',
        'abilities': []
    }


def test_create_a_pokemon_schema_with_abilities():
    ability_schema1 = AbilitySchema(id=1, name='test1', pokemon_id=1)
    ability_schema2 = AbilitySchema(id=2, name='test2', pokemon_id=1)
    pokemon_schema = PokemonSchema(
        id=1,
        name='test',
        description='test description',
        abilities=[ability_schema1, ability_schema2]
    )

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test',
        'description': 'test description',
        'abilities': [
            {
                'id': 1,
                'name': 'test1',
                'pokemon_id': pokemon_schema.id
            },
            {
                'id': 2,
                'name': 'test2',
                'pokemon_id': pokemon_schema.id
            }
        ]
    }


def test_create_ability_schema_from_an_instance(db):
    ability = Ability(id=1, name='test')
    ability_schema = AbilitySchema.from_instance(ability)

    assert ability_schema.to_dict() == {
        'id': ability.id,
        'name': ability.name,
        'pokemon_id': None
    }


def test_create_pokemon_schema_from_an_instance(db):
    pokemon = Pokemon(id=1, name='test name')
    pokemon_schema = PokemonSchema.from_instance(pokemon)

    assert pokemon_schema.to_dict() == {
        'id': pokemon.id,
        'name': pokemon.name,
        'description': None,
        'abilities': []
    }


def test_create_pokemon_schema_with_abilities_from_instance(db):
    ability1 = Ability(id=1, name='test ability 1')
    ability2 = Ability(id=2, name='test ability 2')
    pokemon = Pokemon(id=1, name='test pokemon')
    pokemon.add_abilities([ability1, ability2])

    pokemon_schema = PokemonSchema.from_instance(pokemon)

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test pokemon',
        'description': None,
        'abilities': [
            {
                'id': 1,
                'name': 'test ability 1',
                'pokemon_id': pokemon.id
            },
            {
                'id': 2,
                'name': 'test ability 2',
                'pokemon_id': pokemon.id
            }
        ]
    }
