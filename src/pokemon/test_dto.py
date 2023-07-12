from datetime import datetime

from .dto import AbilityDTO, PokemonDTO
from .model import Pokemon, Ability

from fixtures import db


def teste_create_a_ability_dto():
    ability_dto = AbilityDTO(id=1, name='test')

    assert ability_dto.to_dict() == {
        'id': 1,
        'name': 'test',
        'pokemon_id': None,
    }


def test_create_a_pokemon_dto():
    now = datetime.now()
    pokemon_dto = PokemonDTO(id=1, name='test', last_update=now)

    assert pokemon_dto.to_dict() == {
        'id': 1,
        'name': 'test',
        'abilities': [],
        'last_update': now
    }


def test_create_a_pokemon_dto_with_abilities():
    now = datetime.now()
    ability_dto1 = AbilityDTO(id=1, name='test1', pokemon_id=1)
    ability_dto2 = AbilityDTO(id=2, name='test2', pokemon_id=1)
    pokemon_dto = PokemonDTO(
        id=1,
        name='test',
        last_update=now,
        abilities=[ability_dto1, ability_dto2]
    )

    assert pokemon_dto.to_dict() == {
        'id': 1,
        'name': 'test',
        'last_update': now,
        'abilities': [
            {
                'id': 1,
                'name': 'test1',
                'pokemon_id': pokemon_dto.id
            },
            {
                'id': 2,
                'name': 'test2',
                'pokemon_id': pokemon_dto.id
            }
        ]
    }


def test_create_ability_dto_from_an_instance(db):
    ability = Ability(id=1, name='test')
    ability_dto = AbilityDTO.from_instance(ability)

    assert ability_dto.to_dict() == {
        'id': ability.id,
        'name': ability.name,
        'pokemon_id': None
    }


def test_create_pokemon_dto_from_an_instance(db):
    now = datetime.now()
    pokemon = Pokemon(id=1, name='test name', last_update=now)
    pokemon_dto = PokemonDTO.from_instance(pokemon)

    assert pokemon_dto.to_dict() == {
        'id': pokemon.id,
        'name': pokemon.name,
        'abilities': [],
        'last_update': now
    }


def test_create_pokemon_dto_with_abilities_from_instance(db):
    now = datetime.now()
    ability1 = Ability(id=1, name='test ability 1')
    ability2 = Ability(id=2, name='test ability 2')
    pokemon = Pokemon(id=1, name='test pokemon', last_update=now)
    pokemon.add_abilities([ability1, ability2])

    pokemon_dto = PokemonDTO.from_instance(pokemon)

    assert pokemon_dto.to_dict() == {
        'id': 1,
        'name': 'test pokemon',
        'last_update': pokemon.last_update,
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

def test_pokemon_dto_to_instance():
    ability_dto1 = AbilityDTO(id=1, name='test1', pokemon_id=1)
    ability_dto2 = AbilityDTO(id=2, name='test2', pokemon_id=1)
    pokemon_dto = PokemonDTO(
        id=1,
        name='test',
        abilities=[ability_dto1, ability_dto2]
    )
    assert isinstance(pokemon_dto.to_instance(), Pokemon)


def test_ability_dto_to_instance():
    ability_dto = AbilityDTO(id=1, name='test1', pokemon_id=1)

    assert isinstance(ability_dto.to_instance(), Ability)


def test_pokemon_dto_from_dict():
    data = {
        'name': 'rattata',
        'url': 'https://pokeapi.co/api/v2/pokemon/19/'
    }
    pokemon_dto = PokemonDTO.from_dict(data)

    assert pokemon_dto.id == 19
    assert pokemon_dto.name == 'rattata'


def test_hability_dto_from_dict():
    data = {
        'name': 'overgrow',
        'url': 'https://pokeapi.co/api/v2/ability/65/'
    }
    ability_dto = AbilityDTO.from_dict(data)

    assert ability_dto.id == 65
    assert ability_dto.name == 'overgrow'
    assert ability_dto.pokemon_id is None
