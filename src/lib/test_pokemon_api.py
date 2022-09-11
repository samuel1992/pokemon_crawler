import requests

from unittest.mock import patch

from .pokemon_api import PokemonApi


@patch('requests.get')
def test_get_specific_pokemon(get_mock):
    PokemonApi.get_pokemon(1)
    get_mock.assert_called_once()


@patch('requests.get')
def test_get__all_pokemons(get_mock):
    PokemonApi.get_all_pokemons()
    get_mock.assert_called_once()
