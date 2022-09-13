from extensions import Base, engine, db

from pokemon.model import *


if __name__ == '__main__':
    try:
        print('Deleting the whole database')
        Base.metadata.drop_all(bind=engine)
        print('Recreating the datavase')
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f'Some problem to manage the database: {e}')
