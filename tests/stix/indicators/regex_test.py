"""Tests for the Stix2 bindings."""

import pytest

from yeti.core.indicators.regex import Regex, StixRegex
from yeti.core.errors import ValidationError

@pytest.mark.usefixtures('clean_db')
def test_regex_creation():
    """Tests the creation of a single Regex object."""
    regex = Regex(
        name='Zeus C2',
        labels=['malicious-activity'],
        description='This is how C2 URLs for Zeus usually end.',
        pattern=r'gate\.php$',
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z'
    )
    # pylint: disable=protected-access
    assert regex._stix_object is not None
    assert isinstance(regex._stix_object, StixRegex)

@pytest.mark.usefixtures('clean_db')
def test_update_regex():
    """Tests that a Regex object is succesfully updated."""
    regex = Regex(
        name='Zeus C2',
        labels=['malicious-activity'],
        description='This is how C2 URLs for Zeus usually end.',
        pattern=r'gate\.php$',
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[
            {
            'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
            'phase_name': 'reconnaissance'
            }
        ]
    )
    regex.save()
    stix_id = regex.id
    updated = regex.update({'name': 'Zeus Gate URLs'})
    assert updated.id == stix_id
    assert updated.name == 'Zeus Gate URLs'
    assert updated.labels == ['malicious-activity']
    assert updated.description == 'This is how C2 URLs for Zeus usually end.'
    assert updated.kill_chain_phases == [
            {
            'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
            'phase_name': 'reconnaissance'
            }
        ]
    assert updated.pattern == r'gate\.php$'
    assert str(updated.valid_from) == '2016-01-01 00:00:00+00:00'
    assert str(updated.valid_until) == '2017-01-01 00:00:00+00:00'

@pytest.mark.usefixtures('clean_db')
def test_invalid_regex():
    """Tests that an invalid regular expression is not accepted."""
    with pytest.raises(ValidationError) as error:
        Regex(
            name='Zeus C2',
            labels=['malicious-activity'],
            description='This is how C2 URLs for Zeus usually end.',
            pattern=r'gate\.php$)',
            valid_from='2016-01-01T00:00:00Z',
            valid_until='2017-01-01T00:00:00Z'
        )
    assert 'is not a valid regular expression' in str(error.value)

@pytest.mark.usefixtures('clean_db')
def test_invalid_regex_object():
    """Tests that an invalid Regex object cannot be created."""
    with pytest.raises(ValidationError) as error:
        Regex(
            name='Zeus C2',
            labels=['malicious-activity'],
            description='This is how C2 URLs for Zeus usually end.',
            pattern=r'gate\.php$)',
            # valid_from='2016-01-01T00:00:00Z',
            # valid_until='2017-01-01T00:00:00Z'
        )
    assert 'No values for required properties' in str(error.value)
    assert 'valid_from' in str(error.value)


def test_match(populate_regex):
    """Tests that regular expressions can be matched."""
    r = populate_regex[0]
    match = r.match('http://malicious.com/gate.php')
    assert match['name'] == 'Zeus C2'
    assert match['details'] == b'gate.php'