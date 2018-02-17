# pylint: disable=unused-argument
"""Tests for the Entity datatype."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures("clean_db", "populate_yara_rules")
def test_index():
    """Test that a GET request fetches all Entities."""
    rv = client.get('/api/indicators/')
    response = json.loads(rv.data)
    assert len(response) == 1

@pytest.mark.usefixtures("clean_db")
def test_get(populate_yara_rules):
    """Test fetching single Entity by ID."""
    rv = client.get('/api/indicators/{0:d}/'.format(populate_yara_rules[0].id))
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['id'] == populate_yara_rules[0].id

@pytest.mark.usefixtures("clean_db")
def test_get_notfound():
    """Test error code when Entity does not exist."""
    rv = client.get('/api/indicators/1/')
    assert rv.status_code == 404
