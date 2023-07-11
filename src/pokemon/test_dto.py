from .dto import AbilityDTO, PokemonDTO
from .model import Pokemon, Ability

from fixtures import db


def teste_create_a_ability_schema():
    ability_schema = AbilityDTO(id=1, name='test')

    assert ability_schema.to_dict() == {
        'id': 1,
        'name': 'test',
        'pokemon_id': None
    }


def test_create_a_pokemon_schema():
    pokemon_schema = PokemonDTO(id=1, name='test')

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test',
        'abilities': []
    }


def test_create_a_pokemon_schema_with_abilities():
    ability_schema1 = AbilityDTO(id=1, name='test1', pokemon_id=1)
    ability_schema2 = AbilityDTO(id=2, name='test2', pokemon_id=1)
    pokemon_schema = PokemonDTO(
        id=1,
        name='test',
        abilities=[ability_schema1, ability_schema2]
    )

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test',
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
    ability_schema = AbilityDTO.from_instance(ability)

    assert ability_schema.to_dict() == {
        'id': ability.id,
        'name': ability.name,
        'pokemon_id': None
    }


def test_create_pokemon_schema_from_an_instance(db):
    pokemon = Pokemon(id=1, name='test name')
    pokemon_schema = PokemonDTO.from_instance(pokemon)

    assert pokemon_schema.to_dict() == {
        'id': pokemon.id,
        'name': pokemon.name,
        'abilities': []
    }


def test_create_pokemon_schema_with_abilities_from_instance(db):
    ability1 = Ability(id=1, name='test ability 1')
    ability2 = Ability(id=2, name='test ability 2')
    pokemon = Pokemon(id=1, name='test pokemon')
    pokemon.add_abilities([ability1, ability2])

    pokemon_schema = PokemonDTO.from_instance(pokemon)

    assert pokemon_schema.to_dict() == {
        'id': 1,
        'name': 'test pokemon',
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


def test_pokemon_schema_to_instance():
    ability_schema1 = AbilityDTO(id=1, name='test1', pokemon_id=1)
    ability_schema2 = AbilityDTO(id=2, name='test2', pokemon_id=1)
    pokemon_schema = PokemonDTO(
        id=1,
        name='test',
        abilities=[ability_schema1, ability_schema2]
    )
    assert isinstance(pokemon_schema.to_instance(), Pokemon)


def test_ability_schema_to_instance():
    ability_schema = AbilityDTO(id=1, name='test1', pokemon_id=1)

    assert isinstance(ability_schema.to_instance(), Ability)


def test_pokemon_schema_from_dict():
    data = {
        'name': 'rattata',
        'url': 'https://pokeapi.co/api/v2/pokemon/19/'
    }
    pokemon_schema = PokemonDTO.from_dict(data)

    assert pokemon_schema.id == 19
    assert pokemon_schema.name == 'rattata'


def test_hability_schema_from_dict():
    data = {
        'name': 'overgrow',
        'url': 'https://pokeapi.co/api/v2/ability/65/'
    }
    ability_schema = AbilityDTO.from_dict(data)

    assert ability_schema.id == 65
    assert ability_schema.name == 'overgrow'
    assert ability_schema.pokemon_id is None
