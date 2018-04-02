"""Tests for the Regex API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_index(populate_regex):
    """Test that fetched regular expressions are well-formed"""
    names = [regex.name for regex in populate_regex]
    for name in names:
        query_json = {'name': name}
        rv = client.post('/api/indicators/filter/',
                         data=json.dumps(query_json),
                         content_type='application/json')
        response = json.loads(rv.data)
        for element in response:
            assert isinstance(element['id'], int)
            assert len(element['pattern']) > 1

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_regex_creation():
    pattern = "asd[0-9]"
    query_json = {'name': 'test', 'pattern': pattern, 'type': 'indicator.regex'}
    rv = client.post('/api/indicators/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'] is not None
    assert response['pattern'] == pattern

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_invalid_regex():
    """Test that regular expressions with invalid patterns cannot be created."""
    query_json = {'name': 'test', 'pattern': 'asd[3-2]', 'type': 'indicator.regex'}
    rv = client.post('/api/indicators/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 400
    assert 'ValidationError' in response
    assert 'Could not compile regular expression' in response['ValidationError']

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_no_regex():
    """Test that regular expressions with empty patterns cannot be created."""
    query_json = {'name': 'test', 'type': 'indicator.regex'}
    rv = client.post('/api/indicators/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 400
    assert 'ValidationError' in response
    assert 'pattern' in response['ValidationError']
    assert "Missing data for required field." in response['ValidationError']['pattern']


MATCHING_TEST = (
    ('C\\Users\\tomchop\\AppData\\Roaming\\Google', [{
        'name': 'AppData', 'details': 'AppData\\Roaming\\Google'
    }]),
    ('C\\Users\\tomchop\\AppData\\Local\\Google', []),
)

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_match_regex():
    """Test that Regex can be matched through the API."""
    for obj, expected in MATCHING_TEST:
        query_json = {'object': obj}
        rv = client.post('/api/indicators/match',
                         data=json.dumps(query_json),
                         content_type='application/json')
        response = json.loads(rv.data)
        assert expected == response
        assert rv.status_code == 200
