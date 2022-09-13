import lib.pokemon_api

from unittest.mock import patch

from fixtures import db

from .service import PokemonService
from .model import Pokemon, Ability


@patch('lib.pokemon_api.PokemonApi.get_all_pokemons')
def test_fetch_new_pokemons_and_save_it(mock_get_all_pokemons, db):
    mock_get_all_pokemons.return_value = [
        {
            "name": "bulbasaur",
            "url": "https://pokeapi.co/api/v2/pokemon/1/"
        }
    ]

    PokemonService(db).fetch_new_pokemons()

    query = db.query(Pokemon)

    assert query.count() == 1
    assert query.first().name == 'bulbasaur'
    assert query.first().id == 1


@patch('lib.pokemon_api.PokemonApi.get_pokemon')
def test_fetch_new_abilities_and_save_it(mock_get_pokemon, db):
    pokemon = Pokemon(id=1, name='bulbasaur')
    db.add(pokemon)
    db.commit()

    mock_get_pokemon.return_value = {
        "abilities": [
            {
                "ability": {
                    "name": "overgrow",
                    "url": "https://pokeapi.co/api/v2/ability/65/"
                },
                "is_hidden": False,
                "slot": 1
            }
        ]
    }

    assert pokemon.last_update is None

    PokemonService(db).fetch_new_abilities(pokemon.id)
    pokemon = db.query(Pokemon).first()

    assert pokemon.last_update is not None

    ability = pokemon.abilities[0]

    assert ability.name == 'overgrow'
    assert ability.id == 65


@patch('lib.pokemon_api.PokemonApi.get_pokemon')
def test_fetch_already_existent_ability_but_updates_it(mock_get_pokemon, db):
    pokemon = Pokemon(id=1, name='bulbasaur')
    ability = Ability(id=1, pokemon_id=pokemon.id, name='test 1')
    pokemon.add_abilities([ability])
    db.add(pokemon)
    db.commit()

    mock_get_pokemon.return_value = {
        "abilities": [
            {
                "ability": {
                    "name": "test 2",
                    "url": f"https://pokeapi.co/api/v2/ability/{ability.id}/"
                },
                "is_hidden": False,
                "slot": 1
            }
        ]
    }

    assert ability.name == 'test 1'

    PokemonService(db).fetch_new_abilities(pokemon.id)

    pokemon = db.query(Pokemon).first()
    ability = pokemon.abilities[0]

    assert ability.name == 'test 2'


def test_get_last_updated_pokemons(db):
    pokemon = Pokemon(id=1, name='bulbasaur')
    db.add(pokemon)
    db.commit()

    ids = PokemonService(db).last_updated_pokemons(1)

    assert len(ids) == 1
    assert ids[0] == 1
