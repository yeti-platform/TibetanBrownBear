# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

import json

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

def test_index(clean_db, populate_observables):
    """Test that a GET request fetches all Observables."""
    rv = client.get('/api/observables/')
    response = json.loads(rv.data)
    assert len(response) == 10
    for element in response:
        assert isinstance(element['id'], int)

def test_get(clean_db, populate_observables):
    """Test fetching single Observable by ID."""
    rv = client.get('/api/observables/{0:d}/'.format(populate_observables[0].id))
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['id'] == populate_observables[0].id

def test_get_notfound(clean_db):
    """Test error code when Observable does not exist."""
    rv = client.get('/api/observables/1/')
    assert rv.status_code == 404

def test_post(clean_db):
    """Tests the creation of a new Observable via POST."""
    observable_json = {'value': 'asd', 'type': 'observable'}
    rv = client.post('/api/observables/', data=observable_json)
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

def test_put(clean_db, populate_observables):
    """Tests updating a new Observable via PUT."""
    rv = client.get('/api/observables/{0:d}/'.format(populate_observables[0].id))
    observable_json = json.loads(rv.data)
    rv = client.put('/api/observables/{0:d}/'.format(observable_json['id']),
                    data={'value': 'qwe'})
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

def test_filter(clean_db, populate_observables):
    """Tests searching for specific Observables based on a value regexp."""
    observable_json = {'value': 'asd[0-4]'}
    rv = client.post('/api/observables/filter/', data=observable_json)
    response = json.loads(rv.data)
    assert len(response) == 5

def test_tag(populate_observables):
    uri = '/api/observables/{0:d}/tag'.format(populate_observables[0].id)
    rv = client.post(uri, data={'tags': ['tag1']})
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)
    assert response['tags']
    assert 'tag1' in [tag['name'] for tag in response['tags']]
