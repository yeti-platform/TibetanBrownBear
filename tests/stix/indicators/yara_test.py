"""Tests for the Yara Indicators."""

import pytest

from yeti.core.indicators.yara import Yara, StixYara
from yeti.core.errors import ValidationError

VALID_RULE = """rule yeti_rule
{
    meta:
        description = "Test rule"

    strings:
        $MZ = { 4D 5A }

    condition:
        $MZ
}"""

pytest.mark.usefixtures('clean_db')
def test_yara_creation():
    """Tests the creation of a single Yara object."""
    yara = Yara(
        name='MZ',
        labels=['binary-data'],
        description='This is how PEs usually start with.',
        pattern=VALID_RULE,
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z'
    ).save()
    # pylint: disable=protected-access
    assert yara._stix_object is not None
    assert isinstance(yara._stix_object, StixYara)

@pytest.mark.usefixtures('clean_db')
def test_update_yara():
    """Tests that a Regex object is succesfully updated."""
    yara = Yara(
        name='MZ',
        labels=['binary-data'],
        description='This is how PEs usually start with.',
        pattern=VALID_RULE,
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[
            {
            'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
            'phase_name': 'reconnaissance'
            }
        ]
    ).save()
    stix_id = yara.id
    updated = yara.update({'name': 'PE start'})
    assert updated.id == stix_id
    assert updated.name == 'PE start'
    assert updated.labels == ['binary-data']
    assert updated.description == 'This is how PEs usually start with.'
    assert updated.pattern == VALID_RULE
    assert updated.kill_chain_phases == [
            {
            'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
            'phase_name': 'reconnaissance'
            }
        ]
    assert str(updated.valid_from) == '2016-01-01 00:00:00+00:00'
    assert str(updated.valid_until) == '2017-01-01 00:00:00+00:00'

@pytest.mark.usefixtures('clean_db')
def test_invalid_rule():
    """Tests that an invalid Yara rule is not accepted."""
    with pytest.raises(ValidationError) as error:
        Yara(
            name='MZ',
            labels=['binary-data'],
            description='This is how PEs usually start with.',
            pattern="rule invalid_rule { meta: }",
            valid_from='2016-01-01T00:00:00Z',
            valid_until='2017-01-01T00:00:00Z',
        ).save()
    assert 'is not a valid Yara rule' in str(error.value)

@pytest.mark.usefixtures('clean_db')
def test_invalid_object():
    """Tests that an invalid Yara object cannot be created."""
    with pytest.raises(ValidationError) as error:
        Yara(
            name='Zeus C2',
            labels=['malicious-activity'],
            description='This is how C2 URLs for Zeus usually end.',
            pattern=VALID_RULE,
            # valid_from='2016-01-01T00:00:00Z',
            # valid_until='2017-01-01T00:00:00Z'
        )
    assert 'No values for required properties' in str(error.value)
    assert 'valid_from' in str(error.value)

def test_match(populate_yara_rules):
    """Tests that regular expressions can be matched."""
    r = populate_yara_rules[0]
    match = r.match('MZ\x00\x00\x00')
    assert match['name'] == 'MZ'
    assert match['details'][0] == {
        'offset': 0,
        'name': '$MZ',
        'bytes': {'b64': "b'TVo='"}
    }