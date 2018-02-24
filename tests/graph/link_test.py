# pylint: disable=unused-argument
"""Tests for the Yara rule datatype."""
import pytest

from yeti.core.model.database import YetiObject
from yeti.core.types.hostname import Hostname

@pytest.mark.usefixtures("clean_db")
def test_link(populate_hostnames, populate_malware):
    obs1 = populate_hostnames[0]
    mal = populate_malware[0]
    mal.link_to(obs1, {'attrib':'ute'}, 'uses')
    neighbors = mal.neighbors('uses')
    assert len(neighbors) == 1
    assert isinstance(neighbors[0], Hostname)
