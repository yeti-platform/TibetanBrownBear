"""Tests for the Malware API."""

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
def test_intrusion_set_creation():
    query_json = {
        'name': 'FancyBear',
        'labels': ['APT'],
        'type': 'intrusion-set',
        'first_seen': '2018-08-25T15:22:23.474159Z'
    }
    rv = client.post('/api/entities/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'].startswith('intrusion-set--')
    assert response['name'] == ['FancyBear']
    assert response['labels'] == ['phishing']
    assert response['first_seen'] == '2018-08-25T15:22:23.474159Z'
