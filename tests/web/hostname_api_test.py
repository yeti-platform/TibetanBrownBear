"""Tests for the Hostname API."""

import json
import re

import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()


@pytest.mark.usefixtures('clean_db', 'populate_hostnames')
def test_filter_on_subtype():
    """Tests searching for regular expressions on the /observables/ endpoint
    returns hostname objects."""
    observable_json = {'value': r'asd[0-4]\.com'}
    rv = client.post('/api/observables/filter/',
                     data=json.dumps(observable_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    for item in response:
        assert re.match(r'asd[0-4]\.com', item['value'])
        assert 'hostname' in item['type']

@pytest.mark.usefixtures('clean_db')
def test_post():
    """Tests the creation of a new Hostname via POST."""
    observable_json = {'value': 'asd.com', 'type': 'observable.hostname'}
    rv = client.post('/api/observables/',
                     data=json.dumps(observable_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

@pytest.mark.usefixtures('clean_db')
def test_post_invalid_hostname():
    """Tests that POSTing invalid data does not create a hostname."""
    observable_json = {'value': '123123123', 'type': 'observable.hostname'}
    rv = client.post('/api/observables/',
                     data=json.dumps(observable_json),
                     content_type='application/json')
    assert rv.status_code == 400

@pytest.mark.usefixtures("clean_db")
def test_put(populate_hostnames):
    """Tests that updating with a malformed value fails"""
    rv = client.get('/api/observables/{0:d}/'.format(populate_hostnames[0].id))
    observable_json = json.loads(rv.data)
    rv = client.put('/api/observables/{0:d}/'.format(observable_json['id']),
                    data=json.dumps({'value': 'qwe'}),
                    content_type='application/json')
    assert rv.status_code == 400
    response = json.loads(rv.data)
    assert 'ValidationError' in response
    assert 'Invalid Hostname' in response['ValidationError']
