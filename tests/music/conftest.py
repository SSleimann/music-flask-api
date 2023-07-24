import pytest

from flask_jwt_extended import create_access_token

from musicapi.models import User
from musicapi.dhelper import DummyHelper


@pytest.fixture(scope="package", autouse=True)
def data(app, db):
    d = DummyHelper()
    d.add_dummy_data()


@pytest.fixture(scope="package")
def auth(app, db):
    user = db.session.get(User, 1)

    token = create_access_token(identity=user)

    return token
