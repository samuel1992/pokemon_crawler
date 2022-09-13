from celery.utils.log import get_task_logger

from extensions import Base, engine

from pokemon.service import PokemonService

from .celery import app


logger = get_task_logger(__name__)


app.conf.beat_schedule = {
    'get_new_pokemons': {
        'task': 'get_new_pokemons',
        'schedule': 90.0
    },
}
app.conf.timezone = 'UTC'


@app.task
def get_new_abilities(pokemon_id: int):
    PokemonService.fetch_new_abilities(pokemon_id)

    logger.info(f'Total abilities in db: {PokemonService.ability_total()}')


@app.task(name='get_new_pokemons')
def get_new_pokemons():
    from pokemon.model import Pokemon, Ability
    Base.metadata.create_all(bind=engine)
    PokemonService.fetch_new_pokemons()

    logger.info(f'Total pokemons in db: {PokemonService.pokemon_total()}')

    for pokemon_id in PokemonService.last_updated_pokemons(10):
        get_new_abilities.delay(pokemon_id)
