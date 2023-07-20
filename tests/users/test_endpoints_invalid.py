from flask.testing import FlaskClient

from musicapi.models import User

def test_invalid_register(client: FlaskClient):
    payload = {
        'username': 'testkasldaklkdlkaslkaslcklxkclxklc',
        'email': 'invalidemailcom',
        'password': 'helloPass',
        'password_confirmation': 'helloPass'
    }
    
    res = client.post(
        '/user/register',
        json = payload
    )
    
    assert res.status_code == 400
    assert 'errors' in res.json
    assert 'email' in res.json['errors']
    assert 'username' in res.json['errors']
    
def test_invalid_login_email(client: FlaskClient, user: User):
    payload = {
        'email': 'xxxx@xxx.com',
        'password': 'test'
    }
    
    res = client.post(
        '/user/login',
        json = payload
    )
    
    assert res.status_code == 404
    assert res.json['message'] == 'User not found!'
    
def test_invalid_login_data(client: FlaskClient, user: User):
    payload = {
        'email': 'xxxx',
        'password': 'test'
    }
    
    res = client.post(
        '/user/login',
        json = payload
    )
    
    assert res.status_code == 400
    assert 'errors' in res.json
    assert 'email' in res.json['errors']