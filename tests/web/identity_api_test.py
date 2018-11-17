"""Tests for the Intrusion Set API."""

import json
import pytest

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_identity_creation(authenticated_client):
    query_json = {
        'name': 'John Smith',
        'type': 'identity',
        'description': 'Just another guy.',
        'labels': ['someone'],
        'sectors': ['cyber'],
        'contact_information': '555-12345',
        'identity_class': 'individual',
    }
    rv = authenticated_client.post('/api/entities/',
                                   data=json.dumps(query_json),
                                   content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'].startswith('identity--')
    assert response['name'] == 'John Smith'
    assert response['description'] == 'Just another guy.'
    assert response['labels'] == ['someone']
    assert response['sectors'] == ['cyber']
    assert response['contact_information'] == '555-12345'
    assert response['identity_class'] == 'individual'
