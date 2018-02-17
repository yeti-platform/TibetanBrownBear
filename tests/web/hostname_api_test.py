# pylint: disable=unused-argument
"""Tests for the Hostname datatype."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()


@pytest.mark.usefixtures("clean_db", "populate_observables", "populate_hostnames")
def test_filter_on_subtype():
    """Tests searching for regular expressions on the /observables/ endpoint
    returns hostname objects."""
    observable_json = {'value': r'asd[0-4]\.com'}
    rv = client.post('/api/observables/filter/', data=observable_json)
    response = json.loads(rv.data)
    assert len(response) == 5
    for item in response:
        assert 'hostname' in item['type']

@pytest.mark.usefixtures("clean_db")
def test_post():
    """Tests the creation of a new Hostname via POST."""
    observable_json = {'value': 'asd.com', 'type': 'observable.hostname'}
    rv = client.post('/api/observables/', data=observable_json)
    response = json.loads(rv.data)
    assert isinstance(response['id'], int)

@pytest.mark.usefixtures("clean_db")
def test_post_invalid_hostname():
    """Tests that POSTing invalid data does not create a hostname."""
    observable_json = {'value': '123123123', 'type': 'observable.hostname'}
    rv = client.post('/api/observables/', data=observable_json)
    assert rv.status_code == 400
