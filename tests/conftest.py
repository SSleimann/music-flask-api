import pytest

from musicapi.app import create_app, db
from musicapi.config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            yield client

            db.session.remove()
            db.drop_all()
        