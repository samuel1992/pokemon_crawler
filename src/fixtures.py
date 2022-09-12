import pytest

from app import create_app

app = create_app()


@pytest.fixture
def app():
    return create_app(testing=True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from extensions import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
