"""Tests for the Settings API."""

import json
import pytest

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_get_vocab(authenticated_client):
    """Tests that a vocab defined for a field can be fetched."""
    rv = authenticated_client.get('/api/settings/vocabs/malware-label-ov/',
                                  content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['adware', 'backdoor'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_value_to_vocab(authenticated_client):
    """Tests that we can add a value to a vocab for a given field."""
    rv = authenticated_client.put('/api/settings/vocabs/malware-label-ov/',
                                  data=json.dumps({'value': 'trojan'}),
                                  content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['adware', 'backdoor', 'trojan'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_value_from_vocab(authenticated_client):
    """Tests that we can remvoe a value from a vocab for a given field."""
    rv = authenticated_client.delete('/api/settings/vocabs/malware-label-ov/',
                                     data=json.dumps({'value': 'adware'}),
                                     content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['backdoor'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_nonexistent_value_from_vocab(authenticated_client):
    """Tests that we can't remvoe a nonexistent value from a vocab."""
    rv = authenticated_client.delete('/api/settings/vocabs/malware-label-ov/',
                                     data=json.dumps({'value': 'notexist'}),
                                     content_type='application/json')
    response = json.loads(rv.data)
    assert 'RuntimeError' in response

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_vocab_undefined_field(authenticated_client):
    """Tests that we can add a vocab on a new field name."""
    authenticated_client.put('/api/settings/vocabs/Malware.newField/',
                             data=json.dumps({'value': 'new'}),
                             content_type='application/json')
    rv = authenticated_client.get('/api/settings/vocabs/Malware.newField/',
                                  content_type='application/json')
    response = json.loads(rv.data)
    assert response == ['new']
