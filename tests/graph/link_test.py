# pylint: disable=unused-argument
"""Tests for Yeti linking features."""
import pytest

from yeti.core.entities.malware import Malware

@pytest.mark.usefixtures("clean_db")
def test_link(populate_malware):
    mal = populate_malware[0]
    mal2 = populate_malware[1]
    mal.link_to('uses', mal2)
    neighbors = mal.neighbors('uses')
    assert len(neighbors) == 1
    assert isinstance(neighbors[0], Malware)
    assert neighbors[0].name == 'Sofacy'
