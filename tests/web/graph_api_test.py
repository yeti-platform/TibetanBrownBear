"""Tests for the Entity API."""

import json
import pytest

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_index(populate_malware, authenticated_client):
    """Test that a GET request fetches all neighbors for a given entity."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to(mal2, 'uses')
    mal1.link_to(mal3, 'uses')
    rv = authenticated_client.get('/api/entities/'+mal1.id+'/neighbors/')
    response = json.loads(rv.data)
    assert len(response['vertices']) == 2
    assert len(response['edges']) == 2

@pytest.mark.usefixtures('clean_db')
def test_add_link(populate_malware, authenticated_client):
    """Test that a GET request fetches all neighbors for a given entity."""
    mal1, mal2, _ = populate_malware
    authenticated_client.post('/api/entities/'+mal1.id+'/addlink/',
                              content_type='application/json',
                              data=json.dumps([{
                                  'target': {'id': mal2.id},
                                  'link_type': 'uses',
                                  'stix_rel': None
                              }]))
    rv = authenticated_client.get('/api/entities/'+mal1.id+'/neighbors/')
    response = json.loads(rv.data)
    assert len(response['vertices']) == 1
    assert response['vertices'][mal2.id]['id'] == mal2.id
    assert len(response['edges']) == 1
    assert response['edges'][0]['source_ref'] == mal1.id
    assert response['edges'][0]['target_ref'] == mal2.id

@pytest.mark.usefixtures('clean_db')
def test_delete_link(populate_malware, authenticated_client):
    """Test that a GET request fetches all neighbors for a given entity."""
    mal1, mal2, _ = populate_malware
    relationship = mal1.link_to(mal2, 'uses')
    rv = authenticated_client.delete('/api/relationships/' + relationship.id + '/')
    assert rv.status_code == 200
    rv = authenticated_client.get('/api/entities/'+mal1.id+'/neighbors/')
    assert rv.status_code == 200
    response = json.loads(rv.data)
    assert not response['vertices']
    assert not response['edges']

@pytest.mark.usefixtures('clean_db')
def test_update_link(populate_malware, authenticated_client):
    mal1, mal2, _ = populate_malware
    relationship = mal1.link_to(mal2, 'uses')
    rv = authenticated_client.put(
        '/api/relationships/' + relationship.id + '/',
        data=json.dumps({
            'description': 'random description',
            'relationship_type': 'related-to'
            }),
        content_type='application/json')
    assert rv.status_code == 200
    response = json.loads(rv.data)
    assert response['description'] == 'random description'
    assert response['relationship_type'] == 'related-to'
    assert response['id'] == relationship.id
