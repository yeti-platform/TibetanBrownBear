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
    names = sorted([n.name for n in neighbors['vertices'].values()])
    assert 'Sofacy' == names[0]
    assert 'Zeus' == names[1]
    assert len(neighbors['vertices']) == 2
    assert len(neighbors['edges']) == 2

# pylint: disable=protected-access
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
def test_link_with_relationship_filter(populate_malware, populate_regex):
    _, sofacy, zeus = populate_malware
    zeusc2, _ = populate_regex
    zeus.link_to(sofacy, 'related-to')
    zeus.link_to(zeusc2, 'uses')
    neighbor_uses = zeus.neighbors(link_type='uses')
    assert len(neighbor_uses['vertices']) == 1
    assert neighbor_uses['vertices'][zeusc2.id].id == zeusc2.id

@pytest.mark.usefixtures("clean_db")
def test_link_delete(populate_malware):
    """Tests that a link is correctly deleted."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to(mal2, 'uses')
    mal1.link_to(mal3, 'uses')
    assert len(Relationship.list()) == 2
    mal2.delete()
    assert len(Relationship.list()) == 1

@pytest.mark.usefixtures("clean_db")
def test_updated_link_delete(populate_malware):
    """Tests that all versions of a Relationship are correctly deleted."""
    mal1, mal2, _ = populate_malware
    relationship = mal1.link_to(mal2, 'uses')
    relationship.update({'description': 'description1'})
    relationship.update({'description': 'description2'})
    relationship.update({'description': 'description3'})
    assert len(Relationship.list()) == 1
    relationship.delete()
    assert not Relationship.list()

@pytest.mark.usefixtures('clean_db')
def test_most_recent_link(populate_malware):
    mal1, mal2, _ = populate_malware
    relationship = mal1.link_to(mal2, 'uses')
    relationship.update({'description': 'random description'})
    assert len(Relationship.list()) == 1
    neighbors = mal1.neighbors()
    assert len(neighbors['edges']) == 1
    assert neighbors['edges'][0]['description'] == 'random description'
