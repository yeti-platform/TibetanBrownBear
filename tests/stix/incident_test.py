"""Tests for the Stix2 bindings."""

import pytest

from yeti.core.entities.incident import Incident, StixIncident
# from yeti.core.errors import ValidationError


@pytest.mark.usefixtures('clean_db')
def test_incident_creation():
    """Tests the creation of a single incident object."""
    incident = Incident(
        name='Random incident',
        labels=['dumpster-fire'],
        internal_references=['ref1', 'ref2'],
    )
    # pylint: disable=protected-access
    assert incident._stix_object is not None
    assert isinstance(incident._stix_object, StixIncident)

@pytest.mark.usefixtures('clean_db')
def test_update_incident():
    """Tests that a incident object is succesfully updated."""
    incident = Incident(
        name='Random incident',
        labels=['dumpster-fire'],
        internal_references=['ref1', 'ref2'],
    )
    incident.save()
    stix_id = incident.id
    updated = incident.update({'name': 'Another random incident'})
    assert updated.id == stix_id
    assert updated.name == 'Another random incident'
    assert updated.labels == ['dumpster-fire']
