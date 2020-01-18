"""Tests for the Malware API."""

import json
import pytest

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_attack_pattern_creation(authenticated_client):
    query_json = {
        'name': 'Phishing',
        'labels': ['phishing'],
        'type': 'attack-pattern',
        'kill_chain_phases': [
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
        ]
    }
    rv = authenticated_client.post('/api/entities/',
                                   data=json.dumps(query_json),
                                   content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'].startswith('attack-pattern--')
    assert response['labels'] == ['phishing']
    assert response['kill_chain_phases'] == [
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
    ]


@pytest.mark.usefixtures('clean_db')
def test_attack_pattern_wrong_kc_format(authenticated_client):
    query_json = {
        'name': 'Phishing',
        'labels': ['phishing'],
        'type': 'attack-pattern',
        'kill_chain_phases': [
            {'lol': 'yeti-kc', 'rofl': 'testing'},
            {'lol': 'yeti-kc', 'rofl': 'debugging'}
        ]
    }
    rv = authenticated_client.post('/api/entities/',
                                   data=json.dumps(query_json),
                                   content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 400
    assert response == {
        'ValidationError':
        'Invalid value for AttackPattern \'kill_chain_phases\': Unexpected properties for KillChainPhase: (lol, rofl).'
    }
