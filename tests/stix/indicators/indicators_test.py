"""Tests for the Stix2 bindings."""

import pytest

from stix2 import Indicator as StixIndicator

from yeti.core.indicators.indicator import Indicator


@pytest.mark.usefixtures('clean_db')
def test_indicator_creation():
    """Tests the creation of a single Indicator object."""
    indicator = Indicator(
        name='Poison Ivy Malware',
        labels=['malicious-activity'],
        description='This file is part of Poison Ivy',
        pattern="[ file:hashes.'SHA-256' = '4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877' ]",  # pylint: disable=line-too-long
        valid_from="2016-01-01T00:00:00Z",
        valid_until="2017-01-01T00:00:00Z"
    )
    # pylint: disable=protected-access
    assert indicator._stix_object is not None
    assert isinstance(indicator._stix_object, StixIndicator)

@pytest.mark.usefixtures('clean_db')
def test_update_indicator():
    """Tests that a Indicator object is succesfully updated."""
    indicator = Indicator(
        name='Poison Ivy Malware',
        labels=['malicious-activity'],
        description='This file is part of Poison Ivy',
        pattern="[ file:hashes.'SHA-256' = '4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877' ]",  # pylint: disable=line-too-long
        valid_from="2016-01-01T00:00:00Z",
        valid_until="2017-01-01T00:00:00Z"
    )
    indicator.save()
    stix_id = indicator.id
    updated = indicator.update({'name': 'Poison Apple Malware'})
    assert updated.id == stix_id
    assert updated.labels == ['malicious-activity']
    assert updated.description == 'This file is part of Poison Ivy'
    assert updated.pattern == "[ file:hashes.'SHA-256' = '4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877' ]"  # pylint: disable=line-too-long
    assert str(updated.valid_from) == "2016-01-01 00:00:00+00:00"
    assert str(updated.valid_until) == "2017-01-01 00:00:00+00:00"
