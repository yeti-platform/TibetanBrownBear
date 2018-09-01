"""Tests for the Entity API."""

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
def test_index(populate_malware):
    """Test that a GET request fetches all neighbors for a given entity."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to(mal2, 'uses')
    mal1.link_to(mal3, 'uses')
    rv = client.get('/api/entities/'+mal1.id+'/neighbors/')
    response = json.loads(rv.data)
    assert len(response['vertices']) == 2
    assert len(response['edges']) == 2
