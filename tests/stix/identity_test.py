"""Tests for the Stix2 bindings."""

import pytest

from stix2 import Identity as StixIdentity

from yeti.core.entities.identity import Identity


@pytest.mark.usefixtures('clean_db')
def test_identity_creation():
    """Tests the creation of a single Identity object."""
    identity = Identity(
        name='John Smith',
        description='Just another guy.',
        sectors=['cyber'],
        contact_information='555-12345',
        identity_class='individual'
    )
    # pylint: disable=protected-access
    assert identity._stix_object is not None
    assert isinstance(identity._stix_object, StixIdentity)

@pytest.mark.usefixtures('clean_db')
def test_update_identity():
    """Tests that a Identity object is succesfully updated."""
    identity = Identity(
        name='John Smith',
        description='Just another guy.',
        sectors=['cyber'],
        contact_information='555-12345',
        identity_class='individual'
    )
    identity.save()
    stix_id = identity.id
    updated = identity.update({'name': 'Juan Smith'})
    assert updated.name == 'Juan Smith'
    assert updated.id == stix_id
    assert updated.description == 'Just another guy.'
    assert updated.sectors == ['cyber']
    assert updated.contact_information == '555-12345'
    assert updated.identity_class == 'individual'
