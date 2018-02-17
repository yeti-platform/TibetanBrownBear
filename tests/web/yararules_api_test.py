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
    query_json = {'name': 'MZ'}
    rv = client.post('/api/indicators/filter/', data=query_json)
    response = json.loads(rv.data)
    for element in response:
        assert isinstance(element['id'], int)
        assert len(element['pattern']) > 10
