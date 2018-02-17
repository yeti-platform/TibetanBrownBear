# pylint: disable=unused-argument
"""Tests for the Hostname datatype."""

import pytest

from yeti.core.types.hostname import Hostname
from yeti.core.errors import ValidationError

def test_hostname_creation(clean_db):
    """Tests the creation of a single hostname."""
    obs = Hostname(value='asd.com')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Hostname)
    assert obs.id is not None

def test_hostname_attributes(clean_db, populate_hostnames):
    """Tests that a created Hostname has all needed attributes."""
    allitems = Hostname.list()
    for hostname in allitems:
        assert hasattr(hostname, 'idna')
        assert hostname.idna is not None

def test_hostname_fetch(clean_db):
    """Tests that a fetched Hostname is of the correct type."""
    obs = Hostname(value='asd.com').save()
    fetched_obs = Hostname.get(obs.id)
    assert isinstance(fetched_obs, Hostname)
    assert fetched_obs.id == obs.id

def test_hostnames_list(clean_db, populate_hostnames):
    """Tests fetching all Hostnames in the database."""
    allitems = Hostname.list()
    assert isinstance(allitems[0], Hostname)
    assert len(allitems) == 10


# Normalization and validation tests

NORMALIZATION_TESTS = (
    ('yeti.org.', 'yeti.org', b'yeti.org'),
    ('YETI.CO.UK', 'yeti.co.uk', b'yeti.co.uk'),
    ('YeTi.OrG.', 'yeti.org', b'yeti.org'),
    ('Yéti.ORG.', 'yéti.org', b'xn--yti-bma.org'),
    ('xn--yti-bma.org', 'yéti.org', b'xn--yti-bma.org'),
)

FAILING_TESTS = (
    ('http://yeti.org/'),
    ('yeti.org/'),
)

def test_hostname_idna(clean_db):
    """Tests that a Hostname's value and IDNA are correctly normalized."""
    for value, expected, idna_value in NORMALIZATION_TESTS:
        obs = Hostname(value=value)
        obs.normalize()
        assert obs.value == expected
        assert obs.idna == idna_value

def test_hostname_fails(clean_db):
    """Test that invalid hostnames cannot be created."""
    for failing_value in FAILING_TESTS:
        with pytest.raises(ValidationError):
            Hostname(value=failing_value)
