import requests

BASE_URL = 'https://pokeapi.co/api/v2'


# TODO: could improve the response handling here
# maybe having a response class and handling the http codes better
class PokemonApi:
    _endpoint = 'pokemon'

    @classmethod
    def get_pokemon(cls, id: int):
        response = requests.get(f'{BASE_URL}/{cls._endpoint}/{id}')
        return response.json()

    @classmethod
    def get_all_pokemons(cls, limit: int = 1000000, offset: int = 0):
        params = {'limit': limit, 'offset': offset}
        response = requests.get(f'{BASE_URL}/{cls._endpoint}', params=params)
        return response.json().get('results', [])
