import os

from celery.utils.log import get_task_logger

from extensions import Base, engine

from pokemon.service import PokemonService

from .celery import app


logger = get_task_logger(__name__)


app.conf.beat_schedule = {
    'get_new_pokemons': {
        'task': 'get_new_pokemons',
        # TODO: improve the configuration abstraction, instead of calling the
        # os lib direct here. Could use the flask config feature or something
        'schedule': int(os.environ.get('CRAWLER_INTERVAL'))
    },
}
app.conf.timezone = 'UTC'


@app.task
def get_new_abilities(pokemon_id: int):
    service = PokemonService()
    service.fetch_new_abilities(pokemon_id)

    logger.info(f'Total abilities in db: {service.ability_total()}')


# TODO: instead of calling all pokemons I could have some paralel tasks to get
# pokemons periodic
@app.task(name='get_new_pokemons')
def get_new_pokemons():
    from pokemon.model import Pokemon, Ability
    Base.metadata.create_all(bind=engine)
    service = PokemonService()
    service.fetch_new_pokemons()

    logger.info(f'Total pokemons in db: {service.pokemon_total()}')

    for pokemon_id in service.last_updated_pokemons(10):
        get_new_abilities.delay(pokemon_id)
