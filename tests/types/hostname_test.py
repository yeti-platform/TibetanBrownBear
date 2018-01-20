# pylint: disable=unused-argument
"""Tests for the Hostname datatype."""

from yeti.core.types.hostname import Hostname


def test_hostname_creation(clean_db):
    """Tests the creation of a single hostname."""
    obs = Hostname(value='asd')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Hostname)
    assert obs.id is not None

def test_hostname_attribuets(populated_db):
    allitems = Hostname.list()
    for hostname in allitems:
        assert hasattr(hostname, 'idna')
        assert hostname.idna is not None

def test_hostname_fetch(clean_db):
    """Tests fetching a single hostname by id."""
    obs = Hostname(value='asd').save()
    fetched_obs = Hostname.get(obs.id)
    assert isinstance(fetched_obs, Hostname)
    assert fetched_obs.id == obs.id

def test_hostnames_list(populated_db):
    """Tests fetching all hostnames in the database."""
    allitems = Hostname.list()
    assert isinstance(allitems[0], Hostname)
    assert len(allitems) == 10
