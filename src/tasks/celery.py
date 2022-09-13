from celery import Celery


app = Celery('pokemon_crawler_worker', broker='redis://redis:6379/0')
