"""Tests for the Indicator matching API."""

import json

import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()


@pytest.mark.usefixtures('populate_all')
def test_regex_filter():
    json_data = {'name': '', 'type': 'x-regex'}
    rv = client.post('/api/indicators/filter/',
                     data=json.dumps(json_data),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert len(response) == 2
    for item in response:
        assert item['id'].startswith('x-regex--')