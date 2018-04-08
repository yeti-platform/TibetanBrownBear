"""Tests for the Entity object."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.entities.entity import Entity
from yeti.core.entities.malware import Malware

@pytest.mark.usefixtures('clean_db')
def test_entity_creation():
    """Tests the creation of a single entity."""
    ent = Entity(name='asd')
    assert ent.id is None
    ent = ent.save()
    assert isinstance(ent, Entity)
    assert ent.id is not None

@pytest.mark.usefixtures('clean_db')
def test_entity_get():
    """Tests fetching a single entity by id."""
    ent = Entity(name='asd').save()
    fecthed_entity = Entity.get(ent.id)
    assert isinstance(fecthed_entity, Entity)
    assert fecthed_entity.id == ent.id

@pytest.mark.usefixtures('clean_db')
def test_invalid_entity_name():
    """Tests that an entity with an invalid name cannot be created."""
    with pytest.raises(ValidationError):
        Entity(name=123).save()
    with pytest.raises(ValidationError):
        Entity(name='').save()

@pytest.mark.usefixtures('clean_db', 'populate_entities')
def test_entity_get_or_create():
    """Tests the get_or_create function on entities."""
    count = len(Entity.list())
    first_object = Entity.get_or_create(name='entity0')
    second_object = Entity.get_or_create(name='entity0')
    assert count == len(Entity.list())
    assert first_object.id == second_object.id
    Entity.get_or_create(name='entity999')
    assert count + 1 == len(Entity.list())

@pytest.mark.usefixtures('clean_db', 'populate_entities', 'populate_malware')
def test_different_entity_types():
    """Tests that Entity objects are created with their respective types."""
    allitems = Entity.list()
    malware_count = 0
    entity_count = 0
    for item in allitems:
        if isinstance(item, Malware):
            malware_count += 1
        elif isinstance(item, Entity):
            entity_count += 1
    assert entity_count == 10
    assert malware_count == 2

@pytest.mark.usefixtures('clean_db', 'populate_entities')
def test_entitys_list():
    """Tests fetching all entities in the database."""
    allitems = Entity.list()
    assert isinstance(allitems[0], Entity)
    assert len(allitems) == 10

@pytest.mark.usefixtures('clean_db', 'populate_entities')
def test_entity_formatting():
    """Tests correct entity formatting to string."""
    ent = Entity(name='asd').save()
    assert str(ent) == "<Entity('asd')>"
