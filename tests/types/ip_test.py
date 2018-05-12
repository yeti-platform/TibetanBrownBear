"""Tests for the IP datatype."""

import pytest

from yeti.core.types.ip import IP
from yeti.core.errors import ValidationError


@pytest.mark.usefixtures('clean_db')
def test_ip_creation():
    """Tests the creation of a single IP."""
    obs = IP(value='127.0.0.1')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, IP)
    assert obs.id is not None

@pytest.mark.usefixtures('clean_db', 'populate_ips')
def test_ip_attributes():
    """Tests that a created IP has all needed attributes."""
    allitems = IP.list()
    for ip in allitems:
        assert hasattr(ip, 'version')
        assert ip.version in [4, 6]

@pytest.mark.usefixtures('clean_db')
def test_ip_fetch():
    """Tests that a fetched IP is of the correct type."""
    obs = IP(value='127.0.0.1').save()
    fetched_obs = IP.get(obs.id)
    assert isinstance(fetched_obs, IP)
    assert fetched_obs.id == obs.id

@pytest.mark.usefixtures('clean_db', 'populate_ips')
def test_ips_list():
    """Tests fetching all IPs in the database."""
    allitems = IP.list()
    assert isinstance(allitems[0], IP)
    assert len(allitems) == 10

@pytest.mark.usefixtures('clean_db')
def test_ip_formatting():
    """Tests that observables are formatted correctly when printed."""
    obs = IP(value='127.0.0.1').save()
    assert str(obs) == "<IP('127.0.0.1')>"


# Normalization and validation tests

NORMALIZATION_TESTS = (
    ('127.0.0.1', '127.0.0.1'),
    ('127.0.0.001', '127.0.0.1'),
    ('2001:db8::1', '2001:db8::1'),
    ('2001:0db8:0000:0000:0000:0000:0000:0001', '2001:db8::1'),
)

FAILING_TESTS = (
    ('432.0.0.1'),
    ('9992001:db8::1'),
)

@pytest.mark.usefixtures('clean_db')
def test_normalization():
    """Tests that a IP's value and IDNA are correctly normalized."""
    for value, expected in NORMALIZATION_TESTS:
        obs = IP(value=value)
        obs.normalize()
        assert obs.value == expected

@pytest.mark.usefixtures('clean_db')
def test_ip_fails():
    """Test that invalid ips cannot be created."""
    for failing_value in FAILING_TESTS:
        with pytest.raises(ValueError):
            IP(value=failing_value)
