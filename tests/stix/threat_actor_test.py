"""Tests for the Stix2 bindings."""

import pytest

from stix2 import ThreatActor as StixThreatActor
from yeti.core.entities.threat_actor import ThreatActor


@pytest.mark.usefixtures('clean_db')
def test_threat_actor_creation():
    """Tests the creation of a single ThreatActor object."""
    threat_actor = ThreatActor(
        name='APT28',
        description='Bears...',
        roles=['spies'],
        sophistication='advanced',
        labels=['label1'],
        aliases=['Sofacy'],
        goals=['wreak', 'havoc'],
        resource_level='high',
        primary_motivation='smash',
        secondary_motivations=['fun', 'profit'],
        personal_motivations=['world-burn']
    )
    # pylint: disable=protected-access
    assert threat_actor._stix_object is not None
    assert isinstance(threat_actor._stix_object, StixThreatActor)

@pytest.mark.usefixtures('clean_db')
def test_update_threat_actor():
    """Tests that a ThreatActor object is succesfully updated."""

    threat_actor = ThreatActor(
        name='APT28',
        description='Bears...',
        roles=['spies'],
        sophistication='advanced',
        labels=['label1'],
        aliases=['Sofacy'],
        goals=['wreak', 'havoc'],
        resource_level='high',
        primary_motivation='smash',
        secondary_motivations=['fun', 'profit'],
        personal_motivations=['world-burn']
    )
    threat_actor.save()
    stix_id = threat_actor.id
    updated = threat_actor.update({'name': 'FancyBear'})
    assert updated.id == stix_id
    assert updated.name == 'FancyBear'
    assert updated.description == 'Bears...'
    assert updated.roles == ['spies']
    assert updated.sophistication == 'advanced'
    assert updated.labels == ['label1']
    assert updated.aliases == ['Sofacy']
    assert updated.goals == ['wreak', 'havoc']
    assert updated.resource_level == 'high'
    assert updated.primary_motivation == 'smash'
    assert updated.secondary_motivations == ['fun', 'profit']
    assert updated.personal_motivations == ['world-burn']
