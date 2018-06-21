"""Tests for the Stix2 bindings."""

import pytest

from yeti.core.errors import ValidationError
# from yeti.core.entities.entity import Entity
from yeti.core.entities.malware import Malware
from stix2 import Malware as StixMalware

@pytest.mark.usefixtures('clean_db')
def test_entity_creation():
    """Tests the creation of a single Malware object."""
    malware = Malware(name='asd', labels=['label1'])
    # pylint: disable=protected-access
    assert malware._stix_object is not None
    assert isinstance(malware._stix_object, StixMalware)

@pytest.mark.usefixtures('clean_db')
def test_malformed_malware():
    """Tests that a Malware object missing fields cannot be created."""
    with pytest.raises(ValidationError):
        Malware(name='asd')

@pytest.mark.usefixtures('clean_db')
def test_save_malware():
    """Tests that a Malware object missing fields cannot be created."""
    malware = Malware(name='asd', labels=['label1'])
    saved = malware.save()
    assert saved is not None

@pytest.mark.usefixtures('clean_db')
def test_update_malware():
    """Tests that a Malware object is succesfully updated."""
    malware = Malware(name='asd', labels=['label1'])
    malware.save()
    stix_id = malware._stix_object.id
    updated = malware.update({'name': 'dsa'})
    assert updated._stix_object.name == 'dsa'
    assert updated._stix_object.id == stix_id

@pytest.mark.usefixtures('clean_db')
def test_malware_versionning():
    """Tests that a getting a Malware object returns the most recent version."""
    malware = Malware(name='asd', labels=['label1'])
    malware.save()
    stix_id = malware._stix_object.id
    malware.update({'name': 'dsa'})
    fetched = Malware.get(stix_id)
    assert fetched._stix_object.id == stix_id
    assert fetched._stix_object.created < fetched._stix_object.modified

@pytest.mark.usefixtures('clean_db')
def test_all_versions():
    """Tests that a updating malware results in two versions."""
    malware = Malware(name='asd', labels=['label1'])
    malware.save()
    stix_id = malware._stix_object.id
    malware.update({'name': 'dsa'})
    assert len(malware.all_versions()) == 2
