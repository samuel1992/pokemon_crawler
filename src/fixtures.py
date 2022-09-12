import os
import pytest


@pytest.fixture
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from extensions import Base

    SQLALCHEMY_DATABASE_URL = f'sqlite:///{os.path.abspath(os.path.dirname(__file__))}/app-test.db'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    yield db

    Base.metadata.drop_all(bind=engine)
    db.commit()
