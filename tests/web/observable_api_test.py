"""Tests for the Observable API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures("clean_db")
def test_index(populate_hostnames):
    """Test that a GET request fetches all Observables."""
    rv = client.get('/api/observables/')
    response = json.loads(rv.data)
    assert len(response) == len(populate_hostnames)
    for element in response:
        assert isinstance(element['value'], str)

@pytest.mark.usefixtures("clean_db")
def test_get(populate_hostnames):
    """Test fetching single Observable by ID."""
    rv = client.get('/api/observables/{0:d}/'.format(populate_hostnames[0].id))
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['value'] == populate_hostnames[0].value

@pytest.mark.usefixtures("clean_db")
def test_get_notfound():
    """Test error code when Observable does not exist."""
    rv = client.get('/api/observables/1/')
    assert rv.status_code == 404

@pytest.mark.usefixtures("clean_db")
def test_put(populate_hostnames):
    """Tests updating a new object via PUT."""
    rv = client.get('/api/observables/{0:d}/'.format(populate_hostnames[0].id))
    observable_json = json.loads(rv.data)
    rv = client.put('/api/observables/{0:d}/'.format(observable_json['id']),
                    data=json.dumps({'value': 'qwe.com'}),
                    content_type='application/json')
    response = json.loads(rv.data)
    assert response['id'] == observable_json['id']
    assert response['value'] == 'qwe.com'

@pytest.mark.usefixtures("clean_db")
def test_put_fail_on_invalid_fields(populate_hostnames):
    """Tests updating a new object via PUT."""
    rv = client.get('/api/observables/{0:d}/'.format(populate_hostnames[0].id))
    observable_json = json.loads(rv.data)
    rv = client.put('/api/observables/{0:d}/'.format(observable_json['id']),
                    data=json.dumps({'asd': 'qwe.com'}),
                    content_type='application/json')
    assert rv.status_code == 400

@pytest.mark.usefixtures("clean_db", "populate_hostnames")
def test_filter():
    """Tests searching for specific Observables based on a value regexp."""
    observable_json = {'value': 'asd[0-4]'}
    rv = client.post('/api/observables/filter/',
                     data=json.dumps(observable_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert len(response) == 5

@pytest.mark.usefixtures("clean_db")
def test_filter_fulltext(populate_hostnames):
    """Tests searching for specific Observables using fulltext"""
    keywords = {'keywords': 'com,-asd1,-asd2'}
    rv = client.post('/api/observables/filter/fulltext/',
                     data=json.dumps(keywords),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert len(response) == len(populate_hostnames) - 2

@pytest.mark.usefixtures("clean_db", "populate_hostnames")
def test_subclass_serialization():
    observable_json = {'value': 'asd[0-4]'}
    rv = client.post('/api/observables/filter/',
                     data=json.dumps(observable_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    for item in response:
        assert item['type'] == 'domain-name'

@pytest.mark.usefixtures("clean_db", 'populate_hostnames', 'populate_urls')
def test_match(populate_hostnames, populate_urls):
    uri = '/api/observables/match'
    payload = {
        'observables': [
            'http://nonEXISTtent.com/',
            populate_hostnames[0].value,
            populate_urls[1].value,
            'asd'
        ]
    }
    rv = client.post(uri, data=json.dumps(payload), content_type='application/json')
    response = json.loads(rv.data)
    assert isinstance(response, list)
    assert len(response) == 4
    for item in response:
        if item['query'] == 'http://nonEXISTtent.com/':
            assert not item['found']
            assert item['error'] is None
        if item['query'] == populate_hostnames[0].value:
            assert populate_hostnames[0].dump() in item['found']
        if item['query'] == populate_urls[0].value:
            assert populate_urls[0].dump() in item['found']
        if item['query'] == 'asd':
            assert item['error'] is not None
            assert not item['found']
