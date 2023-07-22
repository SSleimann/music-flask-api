import pytest

from musicapi.models import User

@pytest.fixture(scope='module')
def user(client):
    ...