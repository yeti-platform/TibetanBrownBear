"""Tests for the Hostname datatype."""

import pytest

from yeti.core.observables.hostname import Hostname
from yeti.core.errors import ValidationError


@pytest.mark.usefixtures('clean_db')
def test_hostname_creation():
    """Tests the creation of a single hostname."""
    obs = Hostname(value='asd.com')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Hostname)
    assert obs.id is not None

@pytest.mark.usefixtures('clean_db', 'populate_hostnames')
def test_hostname_attributes():
    """Tests that a created Hostname has all needed attributes."""
    allitems = Hostname.list()
    for hostname in allitems:
        assert hostname.value.startswith('asd')

@pytest.mark.usefixtures('clean_db')
def test_hostname_fetch():
    """Tests that a fetched Hostname is of the correct type."""
    obs = Hostname(value='asd.com').save()
    fetched_obs = Hostname.get(obs.id)
    assert isinstance(fetched_obs, Hostname)
    assert fetched_obs.id == obs.id

@pytest.mark.usefixtures('clean_db', 'populate_hostnames')
def test_hostnames_list():
    """Tests fetching all Hostnames in the database."""
    allitems = Hostname.list()
    assert isinstance(allitems[0], Hostname)
    assert len(allitems) == 10


# Normalization and validation tests

NORMALIZATION_TESTS = (
    ('yeti.org.', 'yeti.org', b'yeti.org'),
    ('yeti[.]org', 'yeti.org', b'yeti.org'),
    ('YETI.CO.UK', 'yeti.co.uk', b'yeti.co.uk'),
    ('YeTi.OrG.', 'yeti.org', b'yeti.org'),
    ('Yéti.ORG.', 'yéti.org', b'xn--yti-bma.org'),
    ('xn--yti-bma.org', 'yéti.org', b'xn--yti-bma.org'),
)

FAILING_TESTS = (
    ('http://yeti.org/'),
    ('yeti.org/'),
    ('asd yeti.org'),
    ('---.org'),
)

@pytest.mark.usefixtures('clean_db')
def test_hostname_idna():
    """Tests that a Hostname's value and IDNA are correctly normalized."""
    for value, expected, _ in NORMALIZATION_TESTS:
        obs = Hostname(value=value)
        obs.normalize()
        assert obs.value == expected

@pytest.mark.usefixtures('clean_db')
def test_hostname_fails():
    """Test that invalid hostnames cannot be created."""
    for failing_value in FAILING_TESTS:
        with pytest.raises(ValidationError):
            Hostname(value=failing_value)
