# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

import json

from yeti.webapp import app

app.testing = True
client = app.test_client()

# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

def test_index(populated_db):
    """Test that a GET request fetches all Observables."""
    rv = client.get('/api/observables/')
    response = json.loads(rv.data)
    assert len(response) == 10

def test_get(populated_db):
    """Test fetching a given Observable by ID."""
    rv = client.get('/api/observables/1/')
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['id'] == 1

def test_post(clean_db):
    """Tests the creation of a new Observable via POST."""
    observable_json = {'value': 'asd'}
    rv = client.post('/api/observables/', data=observable_json)
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

def test_filter(populated_db):
    """Tests searching for specific Observables based on a value regexp."""
    observable_json = {'value': 'asd[0-4]'}
    rv = client.post('/api/observables/filter/', data=observable_json)
    response = json.loads(rv.data)
    assert len(response) == 5
