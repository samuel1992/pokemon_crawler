import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_NAME = os.environ.get('DB_NAME')
DATABASE_USER = os.environ.get('DB_USER')
DATABASE_HOST = os.environ.get('DB_HOST')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()
