"""Tests for the Settings API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_get_vocab():
    """Tests that a vocab defined for a field can be fetched."""
    rv = client.get('/api/settings/vocabs/Malware.type/',
                    content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['trojan', 'banker'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_value_to_vocab():
    """Tests that we can add a value to a vocab for a given field."""
    rv = client.put('/api/settings/vocabs/Malware.type/',
                    data=json.dumps({'value': 'backdoor'}),
                    content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['trojan', 'banker', 'backdoor'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_value_from_vocab():
    """Tests that we can remvoe a value from a vocab for a given field."""
    rv = client.delete('/api/settings/vocabs/Malware.type/',
                       data=json.dumps({'value': 'trojan'}),
                       content_type='application/json')
    response = json.loads(rv.data)
    assert sorted(response) == sorted(['banker'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_nonexistent_value_from_vocab():
    """Tests that we can't remvoe a nonexistent value from a vocab."""
    rv = client.delete('/api/settings/vocabs/Malware.type/',
                       data=json.dumps({'value': 'notexist'}),
                       content_type='application/json')
    response = json.loads(rv.data)
    assert 'RuntimeError' in response

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_vocab_undefined_field():
    """Tests that we can add a vocab on a new field name."""
    client.put('/api/settings/vocabs/Malware.newField/',
               data=json.dumps({'value': 'new'}),
               content_type='application/json')
    rv = client.get('/api/settings/vocabs/Malware.newField/',
                    content_type='application/json')
    response = json.loads(rv.data)
    assert response == ['new']
