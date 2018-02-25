"""Tests for the Entity API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures("clean_db", "populate_entities")
def test_index():
    """Test that a GET request fetches all Entities."""
    rv = client.get('/api/entities/')
    response = json.loads(rv.data)
    assert len(response) == 10
    for element in response:
        assert isinstance(element['id'], int)

@pytest.mark.usefixtures("clean_db")
def test_get(populate_entities):
    """Test fetching single Entity by ID."""
    rv = client.get('/api/entities/{0:d}/'.format(populate_entities[0].id))
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['id'] == populate_entities[0].id

@pytest.mark.usefixtures("clean_db")
def test_get_notfound():
    """Test error code when Entity does not exist."""
    rv = client.get('/api/entities/1/')
    assert rv.status_code == 404

@pytest.mark.usefixtures("clean_db")
def test_post():
    """Tests the creation of a new Entity via POST."""
    entity_json = {'name': 'asd', 'type': 'entity'}
    rv = client.post('/api/entities/', data=entity_json)
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

@pytest.mark.usefixtures("clean_db")
def test_put(populate_entities):
    """Tests updating a new object via PUT."""
    rv = client.get('/api/entities/{0:d}/'.format(populate_entities[0].id))
    entity_json = json.loads(rv.data)
    rv = client.put('/api/entities/{0:d}/'.format(entity_json['id']),
                    data={'name': 'NewEntity'})
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

@pytest.mark.usefixtures("clean_db", "populate_entities")
def test_filter():
    """Tests searching for specific Entitys based on a name regexp."""
    entity_json = {'name': 'entity[0-4]'}
    rv = client.post('/api/entities/filter/', data=entity_json)
    response = json.loads(rv.data)
    assert len(response) == 5

@pytest.mark.usefixtures("clean_db", "populate_entities", "populate_malware")
def test_subclass_serialization():
    rv = client.get('/api/entities/')
    response = json.loads(rv.data)
    for item in response:
        if item['type'] == 'entity.malware':
            assert item.get('family', None) is not None
        else:
            assert item.get('family', None) is None
