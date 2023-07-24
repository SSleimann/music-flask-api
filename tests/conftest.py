import pytest

from musicapi.app import create_app
from musicapi.app import db as _db
from musicapi.config import TestingConfig
from musicapi.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig)

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()

    user = User(username="XXXX", email="xxxx@xxxx.com", password="test")
    user.set_admin()
    _db.session.add(user)
    _db.session.commit()
    
    yield _db

    _db.drop_all()


@pytest.fixture(scope="function")
def session(db):
    conn = db.engine.connect()
    trans = conn.begin()
    
    options = dict(bind=conn, binds={})
    session = db._make_scoped_session(options)

    db.session = session

    yield session

    trans.rollback()
    conn.close()
    session.remove()
