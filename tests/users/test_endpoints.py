from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from musicapi.models import User

def test_register_user(app: FlaskClient, session):
    payload = {
        'username': 'testUser',
        'email': 'test@email.com',
        'password': 'helloPass',
        'password_confirmation': 'helloPass'
    }
    
    res = app.post(
        '/user/register',
        json = payload
    )
    
    assert res.status_code == 201
    assert res.json['username'] == payload['username']
    assert res.json['email'] == payload['email']
    assert res.json['is_admin'] == False
    
def test_login_user(app: FlaskClient, session):
    payload = {
        'email': 'xxxx@xxxx.com',
        'password': 'test'
    }
    
    res = app.post(
        '/user/login',
        json = payload
    )
    
    assert res.status_code == 200
    assert 'token' in res.json

def test_profile_user(app: FlaskClient, session):
    user = session.get(User, 1)
    access_token = create_access_token(identity=user)
    
    res = app.get(
        '/user/profile',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        }
        
    )
    
    assert res.status_code == 200
    assert res.json['username'] == user.username
    assert res.json['email'] == user.email
    assert res.json['is_admin'] == user.is_admin