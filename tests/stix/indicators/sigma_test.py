"""Tests for Sigma Indicators."""

import pytest

from yeti.core.indicators.sigma import Sigma, StixSigma
from yeti.core.errors import ValidationError

VALID_RULE = """
title: Relevant ClamAV Message
description: Detects relevant ClamAV messages
references:
    - https://github.com/ossec/ossec-hids/blob/master/etc/rules/clam_av_rules.xml
logsource:
    product: linux
    service: clamav
detection:
    keywords:
        - 'Trojan*FOUND'
        - 'VirTool*FOUND'
        - 'Webshell*FOUND'
        - 'Rootkit*FOUND'
        - 'Htran*FOUND'
    condition: keywords
falsepositives:
    - Unknown
level: high
"""

INVALID_RULE = """
    keywords:
        - 'Trojan*FOUND'
        - 'VirTool*FOUND'
        - 'Webshell*FOUND'
        - 'Rootkit*FOUND'
        - 'Htran*FOUND'
"""

pytest.mark.usefixtures('clean_db')
def test_sigma_creation():
    """Tests the creation of a single Sigma object."""
    sigma = Sigma(
        name='Relevant ClamAV Message',
        labels=['av-detect'],
        description='Detects relevant ClamAV messages',
        pattern=VALID_RULE,
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z'
    ).save()
    # pylint: disable=protected-access
    assert sigma._stix_object is not None
    assert isinstance(sigma._stix_object, StixSigma)

@pytest.mark.usefixtures('clean_db')
def test_update_sigma():
    """Tests that a Sigma object is succesfully updated."""
    sigma = Sigma(
        name='Relevant ClamAV Message',
        labels=['av-detect'],
        description='Detects relevant ClamAV messages',
        pattern=VALID_RULE,
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[{
            'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
            'phase_name': 'installation'
        }]
    ).save()
    stix_id = sigma.id
    updated = sigma.update({'name': 'ClamAV Messages'})
    assert updated.id == stix_id
    assert updated.name == 'ClamAV Messages'
    assert updated.labels == ['av-detect']
    assert updated.description == 'Detects relevant ClamAV messages'
    assert updated.pattern == VALID_RULE
    assert updated.kill_chain_phases == [{
        'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
        'phase_name': 'installation'
    }]
    assert str(updated.valid_from) == '2016-01-01 00:00:00+00:00'
    assert str(updated.valid_until) == '2017-01-01 00:00:00+00:00'

@pytest.mark.usefixtures('clean_db')
def test_invalid_rule():
    """Tests that an invalid Sigma rule is not accepted."""
    with pytest.raises(ValidationError) as error:
        Sigma(
            name='Relevant ClamAV Message',
            labels=['av-detect'],
            description='Detects relevant ClamAV messages',
            pattern=INVALID_RULE,
            valid_from='2016-01-01T00:00:00Z',
            valid_until='2017-01-01T00:00:00Z',
        ).save()
    assert 'is not a valid Sigma rule' in str(error.value)
