import pytest

from app import create_app

app = create_app()


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def db():
    from extensions import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
