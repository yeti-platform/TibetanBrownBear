# pylint: disable=unused-argument
"""Tests for Yeti linking features."""
import pytest

from yeti.core.entities.malware import Malware

@pytest.mark.usefixtures("clean_db")
def test_link(populate_malware):
    """Tests that neighbors are consistent with links in the database."""
    mal1, mal2, mal3 = populate_malware
    mal1.link_to('uses', mal2)
    mal1.link_to('uses', mal3)
    neighbors = mal1.neighbors('uses')
    assert len(neighbors) == 2
    assert isinstance(neighbors['vertices'][mal2.id], Malware)
    names = [n.name for n in neighbors['vertices'].values()]
    assert 'Sofacy' in names
    assert 'Zeus' in names
