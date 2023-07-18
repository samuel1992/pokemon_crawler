import os

from celery.utils.log import get_task_logger

from extensions import Base, engine

from pokemon.service import PokemonService

from lib.immudb_api.client import ImmuDBClient

from .celery import app


logger = get_task_logger(__name__)


app.conf.beat_schedule = {
    'get_new_pokemons': {
        'task': 'get_new_pokemons',
        'schedule': int(os.environ.get('CRAWLER_INTERVAL'))
    },
}
app.conf.timezone = 'UTC'


def setup_collection():
    specification = {
        "fields": [
            {
                "name": "name",
                "type": "STRING"
            },
            {
                "name": "id",
                "type": "STRING"
            },
            {
                "name": "abilities",
                "type": "STRING"
            },
            {
                "name": "last_update",
                "type": "STRING"
            }
        ],
        "indexes": [
            {
                "fields": [
                    "id"
                ],
                "isUnique": True
            }
        ]
    }
    ImmuDBClient(
        token=os.environ.get('IMMUDB_API_TOKEN'),
        ledger='default',
        collection='default'
    ).create_collection(specification)


@app.task
def get_new_abilities(pokemon_id: int):
    service = PokemonService()
    service.fetch_new_abilities(pokemon_id)

    logger.info(f'Total abilities in db: {service.ability_total()}')


@app.task(name='get_new_pokemons')
def get_new_pokemons():
    setup_collection()

    service = PokemonService()
    service.fetch_new_pokemons()

    logger.info(f'Total pokemons in db: {service.pokemon_total()}')

    #for pokemon_id in service.last_updated_pokemons(10):
    #    get_new_abilities.delay(pokemon_id)
