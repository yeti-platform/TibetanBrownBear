"""Tests for the Course of Action API."""

import json
import pytest

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_course_of_action_creation(authenticated_client):
    query_json = {
        'name': 'Add TCP port 80 Filter Rule',
        'labels': ['block'],
        'type': 'course-of-action',
    }
    rv = authenticated_client.post('/api/entities/',
                                   data=json.dumps(query_json),
                                   content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'].startswith('course-of-action--')
    assert response['name'] == 'Add TCP port 80 Filter Rule'
    assert response['labels'] == ['block']
