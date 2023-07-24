from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from .dto import AbilityDTO, PokemonDTO
from .service import PokemonService


class TestPokemonService(TestCase):
    def setUp(self):
        self.pokemon_repository = MagicMock()
        self.ability_repository = MagicMock()
        self.service = PokemonService(self.pokemon_repository, self.ability_repository)

    @patch('lib.pokemon_api.PokemonApi.get_all_pokemons')
    def test_fetch_new_pokemons_and_save_it(self, mock_get_all_pokemons):
        pokemons_response = [
            {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon/1/"
            },
            {
                "name": "chupacabra",
                "url": "https://pokeapi.co/api/v2/pokemon/2/"
            }
        ]
        mock_get_all_pokemons.return_value = pokemons_response
        self.pokemon_repository.get_by_id.return_value = None
        self.pokemon_repository.create = MagicMock()

        self.service.fetch_new_pokemons()

        self.pokemon_repository.create.assert_called()
        assert self.pokemon_repository.create.call_count == len(pokemons_response)
        # Assert that the method create was called with an instance of PokemonDTO
        for call_args in self.pokemon_repository.create.call_args_list:
            for arg in call_args.args:
                assert isinstance(arg, PokemonDTO)

    @patch('lib.pokemon_api.PokemonApi.get_all_pokemons')
    def test_fetch_pokemons_that_already_exist(self, mock_get_all_pokemons):
        pokemons_response = [
            {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon/1/"
            },
            {
                "name": "chupacabra",
                "url": "https://pokeapi.co/api/v2/pokemon/2/"
            }
        ]
        mock_get_all_pokemons.return_value = pokemons_response
        self.pokemon_repository.get_by_id.return_value = 1
        self.pokemon_repository.create = MagicMock()

        self.service.fetch_new_pokemons()

        self.pokemon_repository.create.assert_not_called()

    @patch('lib.pokemon_api.PokemonApi.get_pokemon')
    def test_fetch_new_abilities_and_save_it(self, mock_get_pokemon):
        now = datetime.now()
        pokemon_dto = PokemonDTO(id=1, name='test', last_update=now)
        abilities_response = {
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
        mock_get_pokemon.return_value = abilities_response
        self.pokemon_repository.get_by_id.return_value = pokemon_dto
        self.pokemon_repository.update = MagicMock()
        self.ability_repository.get_by_name.return_value = None

        self.service.fetch_new_abilities(1)

        assert pokemon_dto.last_update != now

        self.ability_repository.create.assert_called()
        assert self.ability_repository.create.call_count == len(abilities_response['abilities'])
        # Assert that the method create was called with an instance of AbilityDTO
        for call_args in self.ability_repository.create.call_args_list:
            for arg in call_args.args:
                assert isinstance(arg, AbilityDTO)

    @patch('lib.pokemon_api.PokemonApi.get_pokemon')
    def test_fetch_already_existent_ability_but_updates_it(self, mock_get_pokemon):
        now = datetime.now()
        pokemon_dto = PokemonDTO(id=1, name='test', last_update=now)
        abilities_response = {
            "abilities": [
                {
                    "ability": {
                        "name": "test 2",
                        "url": "https://pokeapi.co/api/v2/ability/1/"
                    },
                    "is_hidden": False,
                    "slot": 1
                }
            ]
        }
        ability_dto = AbilityDTO.from_dict({
            **{'pokemon_id': pokemon_dto.id},
            **abilities_response['abilities'][0]['ability']
        })
        mock_get_pokemon.return_value = abilities_response
        self.pokemon_repository.get_by_id.return_value = pokemon_dto
        self.pokemon_repository.update = MagicMock()
        self.ability_repository.get_by_name.return_value = ability_dto

        self.service.fetch_new_abilities(1)

        assert pokemon_dto.last_update != now

        self.ability_repository.update.assert_called()
        # Assert that the method update was called with an instance of AbilityDTO
        for call_args in self.ability_repository.update.call_args_list:
            for arg in call_args.args:
                assert isinstance(arg, AbilityDTO)

    def test_get_last_updated_pokemons(self):
        pokemon_dto = PokemonDTO(id=1, name='test')
        self.pokemon_repository.get_all.return_value = [pokemon_dto]

        ids = self.service.last_updated_pokemons(1)

        assert len(ids) == 1
        assert ids[0] == '1'

        self.pokemon_repository.get_all.assert_called_with(1)
