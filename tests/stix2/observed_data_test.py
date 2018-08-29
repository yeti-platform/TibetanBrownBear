"""Tests for the Stix2 bindings."""

import pytest

from stix2 import ObservedData as StixObservedData
from stix2 import DomainName

from yeti.core.entities.observed_data import ObservedData


@pytest.mark.usefixtures('clean_db')
def test_observed_data_creation():
    """Tests the creation of a single ObservedData object."""
    observed_data = ObservedData(
        labels=['cyber'],
        number_observed=1,
        first_observed='2015-12-21T19:00:00Z',
        last_observed='2015-12-21T19:00:00Z',
        objects={'0': DomainName(value='yeti.org')}
    )
    # pylint: disable=protected-access
    assert observed_data._stix_object is not None
    assert isinstance(observed_data._stix_object, StixObservedData)
    assert isinstance(observed_data.objects['0'], DomainName)

@pytest.mark.usefixtures('clean_db')
def test_update_observed_data():
    """Tests that a ObservedData object is succesfully updated."""
    observed_data = ObservedData(
        labels=['cyber'],
        number_observed=1,
        first_observed='2015-12-21T19:00:00Z',
        last_observed='2015-12-21T19:00:00Z',
        objects={'0': DomainName(value='yeti.org')}
    )
    observed_data.save()
    stix_id = observed_data.id
    updated = observed_data.update({'number_observed': 2})
    assert updated.number_observed == 2
    assert updated.id == stix_id
    assert updated.labels == ['cyber']
    assert str(updated.first_observed) == '2015-12-21 19:00:00+00:00'
    assert str(updated.last_observed) == '2015-12-21 19:00:00+00:00'
    assert updated.objects == {'0': DomainName(value='yeti.org')}
