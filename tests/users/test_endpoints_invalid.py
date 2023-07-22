from flask.testing import FlaskClient

from musicapi.models import User

def test_invalid_register(app: FlaskClient):
    payload = {
        'username': 'testkasldaklkdlkaslkaslcklxkclxklc',
        'email': 'invalidemailcom',
        'password': 'helloPass',
        'password_confirmation': 'helloPass'
    }
    
    res = app.post(
        '/user/register',
        json = payload
    )
    
    assert res.status_code == 400
    assert 'errors' in res.json
    assert 'email' in res.json['errors']
    assert 'username' in res.json['errors']
    
def test_invalid_login_email(app: FlaskClient, session):
    payload = {
        'email': 'xxxx@xxx.com',
        'password': 'test'
    }
    
    res = app.post(
        '/user/login',
        json = payload
    )
    
    assert res.status_code == 404
    assert res.json['message'] == 'User not found!'
    
def test_invalid_login_data(app: FlaskClient, session):
    payload = {
        'email': 'xxxx',
        'password': 'test'
    }
    
    res = app.post(
        '/user/login',
        json = payload
    )
    
    assert res.status_code == 400
    assert 'errors' in res.json
    assert 'email' in res.json['errors']