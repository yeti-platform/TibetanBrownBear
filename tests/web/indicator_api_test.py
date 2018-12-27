"""Tests for the Indicator API."""

import json

import pytest

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_regex_filter(authenticated_client):
    json_data = {'name': '', 'type': 'x-regex'}
    rv = authenticated_client.post(
        '/api/indicators/filter/',
        data=json.dumps(json_data),
        content_type='application/json',
    )
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert len(response) == 2
    for item in response:
        assert item['id'].startswith('x-regex--')


@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_regex_filter_on_name(authenticated_client):
    json_data = {'name': 'Zeus', 'type': 'x-regex'}
    rv = authenticated_client.post(
        '/api/indicators/filter/',
        data=json.dumps(json_data),
        content_type='application/json',
    )
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert len(response) == 1
    item = response[0]
    assert item['name'] == 'Zeus C2'
    assert item['id'].startswith('x-regex--')


@pytest.mark.usefixtures('clean_db')
def test_regex_new(authenticated_client):
    json_data = {
        'type': 'x-regex',
        'name': 'New regex',
        'labels': ['test1'],
        'description': 'Random description',
        'pattern': '^regex$',
        'valid_from': '2018-10-03T09:32:00.000Z',
        'valid_until': '2018-10-05T09:32:00.000Z',
        'kill_chain_phases': [
            {
                'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
                'phase_name': 'reconnaissance',
            }
        ],
    }
    rv = authenticated_client.post(
        '/api/indicators/',
        data=json.dumps(json_data),
        content_type='application/json',
    )
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['name'] == 'New regex'
    assert response['id'].startswith('x-regex--')


@pytest.mark.usefixtures('clean_db')
def test_regex_invalid(authenticated_client):
    json_data = {
        'type': 'x-regex',
        'name': 'New regex',
        'labels': ['test1'],
        'description': 'Random description',
        'pattern': '^regex$',
        'valid_until': '2018-10-05T09:32:00.000Z',
        'kill_chain_phases': [
            {
                'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
                'phase_name': 'reconnaissance',
            }
        ],
    }
    rv = authenticated_client.post(
        '/api/indicators/',
        data=json.dumps(json_data),
        content_type='application/json',
    )
    response = json.loads(rv.data)
    assert rv.status_code == 400
    assert 'ValidationError' in response
    assert 'valid_from' in response['ValidationError']
    assert 'No values for required properties' in response['ValidationError']
