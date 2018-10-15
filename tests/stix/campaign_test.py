"""Tests for the Stix2 bindings."""
from datetime import datetime

import pytest

from stix2 import Campaign as StixCampaign
from yeti.core.entities.campaign import Campaign


@pytest.mark.usefixtures('clean_db')
def test_campaign_creation():
    """Tests the creation of a single Campaign object."""
    campaign = Campaign(
        name='Saffron Rose',
        description='Hack things',
        labels=['apt'],
        aliases=['kitten'],
        first_seen=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        objective='Hack things',
    )
    # pylint: disable=protected-access
    assert campaign._stix_object is not None
    assert isinstance(campaign._stix_object, StixCampaign)

@pytest.mark.usefixtures('clean_db')
def test_update_campaign():
    """Tests that a Campaign object is succesfully updated."""

    date = datetime.strptime(
        '2018-08-25T15:22:23.474159+0000', '%Y-%m-%dT%H:%M:%S.%f%z')

    campaign = Campaign(
        name='Saffron Rose',
        description='Hack things',
        labels=['apt'],
        aliases=['kitten'],
        first_seen=date,
        last_seen=date,
        objective='Hack things',
    )
    campaign.save()
    modified = campaign.modified
    stix_id = campaign.id
    updated = campaign.update({'name': 'Saffron Tulip'})
    assert updated.id == stix_id
    assert updated.name == 'Saffron Tulip'
    assert updated.description == 'Hack things'
    assert updated.labels == ['apt']
    assert updated.aliases == ['kitten']
    assert str(updated.first_seen) == '2018-08-25 15:22:23.474159+00:00'
    assert str(updated.last_seen) == '2018-08-25 15:22:23.474159+00:00'
    assert updated.objective == 'Hack things'
    assert modified < updated.modified
