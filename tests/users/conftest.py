import pytest

from musicapi.app import db
from musicapi.models import User

@pytest.fixture()
def user():
    user = User(username='XXXX', email='xxxx@xxxx.com', password='test')
    db.session.add(user)
    db.session.commit()
    
    return user