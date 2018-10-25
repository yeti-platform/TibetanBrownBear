# pylint: disable=unused-argument
"""Tests for Yeti linking features."""
import pytest

from yeti.core.entities.malware import Malware
from yeti.core.relationships.relationship import Relationship

@pytest.mark.usefixtures("clean_db")
def test_link(populate_malware):
    """Tests that neighbors are consistent with links in the database."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to(mal2, 'uses')
    mal1.link_to(mal3, 'uses')
    neighbors = mal1.neighbors()
    assert len(neighbors) == 2
    assert isinstance(neighbors['vertices'][mal2.id], Malware)
    names = [n.name for n in neighbors['vertices'].values()]
    assert 'Sofacy' in names
    assert 'Zeus' in names

@pytest.mark.usefixtures("clean_db")
def test_link_preservation_on_update(populate_malware):
    """Tests that links always point to the most up-to-date STIX object."""
    gootkit, sofacy, _ = populate_malware
    gootkit.link_to(sofacy, 'uses')
    old_id = sofacy._arango_id
    neighbors = gootkit.neighbors()
    assert len(neighbors['vertices']) == 1
    assert neighbors['vertices'][sofacy.id]._arango_id == sofacy._arango_id
    sofacy.update({'name': 'PlugX'})
    neighbors = gootkit.neighbors()
    assert neighbors['vertices'][sofacy.id]._arango_id == sofacy._arango_id
    assert neighbors['vertices'][sofacy.id].name == 'PlugX'
    assert old_id != sofacy._arango_id

@pytest.mark.usefixtures("clean_db")
def test_link_delete(populate_malware):
    """Tests that a link is correctly deleted."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to(mal2, 'uses')
    mal1.link_to(mal3, 'uses')
    assert len(Relationship.list()) == 2
    mal2.delete()
    assert len(Relationship.list()) == 1
