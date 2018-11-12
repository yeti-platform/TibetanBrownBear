"""Tests for the User API."""

import json
import jwt

import pytest

from yeti.common.config import yeti_config
from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_index(populate_users):
    """Test that fetched User objects are well-formed"""
    emails = [user.email for user in populate_users]
    for email in emails:
        query_json = {'email': email}
        rv = client.post('/api/users/filter/',
                         data=json.dumps(query_json),
                         content_type='application/json')
        response = json.loads(rv.data)
        for item in response:
            assert item['email']
            assert 'password' not in item

@pytest.mark.usefixtures('clean_db', 'populate_users')
def test_login():
    """Test that a user gets a valid JWT on succesful log-in."""
    query_json = {
        'email': 'admin@email.com',
        'password': 'password0'
    }

    rv = client.post('/api/users/login/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert 'token' in response
    assert response
    decoded = jwt.decode(response['token'], yeti_config.core.secret_key)
    assert decoded['sub'] == 'admin@email.com'

@pytest.mark.usefixtures('clean_db', 'populate_users')
def test_failed_login():
    """Test that a user gets a valid JWT on succesful log-in."""
    query_json = {
        'email': 'admin@email.com',
        'password': 'DIDNTSAYTHEMAGICWORD'
    }
    rv = client.post('/api/users/login/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert response == {'error': 'Invalid credentials for admin@email.com.'}

@pytest.mark.usefixtures('clean_db')
def test_nonexistent_user():
    """Test that a user gets a valid JWT on succesful log-in."""
    query_json = {
        'email': 'notexist@email.com',
        'password': '123456'
    }
    rv = client.post('/api/users/login/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert response == {'error': 'Invalid credentials for notexist@email.com.'}

@pytest.mark.usefixtures('clean_db', 'populate_users')
def test_protected_resource_access_granted():
    query_json = {
        'email': 'admin@email.com',
        'password': 'password0'
    }
    rv = client.post('/api/users/login/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    token = response['token']
    rv = client.get('/api/users/protected/',
                    headers={'Authorization': f'Bearer: {token}'},
                    content_type='application/json')
    assert rv.status_code == 200
    response = json.loads(rv.data)
    assert response['msg'] == "You're in!"


@pytest.mark.usefixtures('clean_db', 'populate_users')
def test_protected_resource_access_denied():
    rv = client.get('/api/users/protected/',
                    content_type='application/json')
    assert rv.status_code == 401
    response = json.loads(rv.data)
    assert not response['authenticated']
    assert response['message'] == ('Invalid or nonexistent token. '
                                   'Please get a new token.')
