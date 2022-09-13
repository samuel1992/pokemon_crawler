# Simple pokemon crawler

Basically the project is a Flask api Using SQLAlchemy to handle the database stuff and Celery for the assyncronous tasks.

# How to install and run it?
```
docker-compose built
docker-compose up

# Application is running on localhost:8080
```

# API
The application only has one endpoint `/pokemons` where is stored all data collected from the crawler.
```
GET http://localhost:8080/pokemons
{
    "pokemons": [
        {
            "abilities": [],
            "id": 57,
            "name": "primeape"
        },
        {
            "abilities": [
                {
                    "id": 38,
                    "name": "poison-point",
                    "pokemon_id": 29
                },
                {
                    "id": 79,
                    "name": "rivalry",
                    "pokemon_id": 29
                }
            ],
            "id": 29,
            "name": "nidoran-f"
        } ...
```

# Running the tests
Mainly the project has unittests but some of the tests also validates some database operations using Pytest fixtures for that.
```
docker-compose run web pytest
```

# Configuration
I didn't group all the configs in a single place as the ideal but basically everything is using environment variables that you can find in the `docker-compose.yml` file.
Some util variables:
```
- CRAWLER_INTERVAL=30 # Represents the interval that the crawler will take until run the next task to sync the pokemons with the api
```

# More about it ..
- It has two async tasks and the main job is to retrieve pokemons from the api and update their abilities. For that I use a service to not have to interact directly with
the model.
- I chose to use the SQLAlchemy lib instead of using the Flask-SQLAlchemy because even though the Flask foucused lib is "easier" sometimes you can get a little confuse
  with the whole app context involving the db layer. So this way the database layer is disatached from the flask app and we can operate it freely from an external task,
etc.
