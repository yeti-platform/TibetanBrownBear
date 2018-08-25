"""Tests for the Stix2 bindings."""
from datetime import datetime

import pytest

from stix2 import IntrusionSet as StixIntrusionSet
from yeti.core.entities.intrusion_set import IntrusionSet


@pytest.mark.usefixtures('clean_db')
def test_intrusion_set_creation():
    """Tests the creation of a single IntrusionSet object."""
    intrusion_set = IntrusionSet(
        name='APT28',
        labels=['label1'],
        aliases=['Sofacy'],
        first_seen=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        goals=['wreak', 'havoc'],
        resource_level='high',
        primary_motivation='smash',
        secondary_motivations=['fun', 'profit'],
    )
    # pylint: disable=protected-access
    assert intrusion_set._stix_object is not None
    assert isinstance(intrusion_set._stix_object, StixIntrusionSet)

@pytest.mark.usefixtures('clean_db')
def test_update_intrusion_set():
    """Tests that a IntrusionSet object is succesfully updated."""

    date = datetime.strptime('2018-08-25T15:22:23.474159+0000', '%Y-%m-%dT%H:%M:%S.%f%z')

    intrusion_set = IntrusionSet(
        name='APT28',
        labels=['label1'],
        aliases=['Sofacy'],
        first_seen=date,
        last_seen=date,
        goals=['wreak', 'havoc'],
        resource_level='high',
        primary_motivation='smash',
        secondary_motivations=['fun', 'profit'],
    )
    intrusion_set.save()
    stix_id = intrusion_set.id
    updated = intrusion_set.update({'name': 'FancyBear'})
    assert updated.id == stix_id
    assert updated.name == 'FancyBear'
    assert updated.labels == ['label1']
    assert updated.aliases == ['Sofacy']
    assert str(updated.first_seen) == '2018-08-25 15:22:23.474159+00:00'
    assert str(updated.last_seen) == '2018-08-25 15:22:23.474159+00:00'
    assert updated.goals == ['wreak', 'havoc']
    assert updated.resource_level == 'high'
    assert updated.primary_motivation == 'smash'
    assert updated.secondary_motivations == ['fun', 'profit']
