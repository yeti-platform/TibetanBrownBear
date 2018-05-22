"""Tests for the URL datatype."""

import pytest

from yeti.core.observables.url import URL
from yeti.core.errors import ValidationError


@pytest.mark.usefixtures('clean_db')
def test_url_creation():
    """Tests the creation of a single url."""
    obs = URL(value='http://asd.com')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, URL)
    assert obs.id is not None

@pytest.mark.usefixtures('clean_db', 'populate_urls')
def test_url_attributes():
    """Tests that a created URL has all needed attributes."""
    allitems = URL.list()
    for url in allitems:
        assert hasattr(url, 'parsed')
        assert url.parsed is not None

@pytest.mark.usefixtures('clean_db')
def test_url_fetch():
    """Tests that a fetched URL is of the correct type."""
    obs = URL(value='http://asd.com').save()
    fetched_obs = URL.get(obs.id)
    assert isinstance(fetched_obs, URL)
    assert fetched_obs.id == obs.id

@pytest.mark.usefixtures('clean_db', 'populate_urls')
def test_urls_list():
    """Tests fetching all URLs in the database."""
    allitems = URL.list()
    assert isinstance(allitems[0], URL)
    assert len(allitems) == 10

@pytest.mark.usefixtures('clean_db')
def test_url_formatting():
    """Tests that observables are formatted correctly when printed."""
    obs = URL(value='http://asd.com/').save()
    assert str(obs) == "<URL('http://asd.com/')>"


# Normalization and validation tests

NORMALIZATION_TESTS = (
    ('http://yeti.org', 'http://yeti.org/', 'yeti.org'),
    ('http://www[.]yeti[.]org', 'http://www.yeti.org/', 'yeti.org'),
    ('http://YETI.CO.UK', 'http://yeti.co.uk/', 'yeti.co.uk'),
    ('http://127.0.0.1/', 'http://127.0.0.1/', '127.0.0.1'),
    ('http://YeTi.OrG', 'http://yeti.org/', 'yeti.org'),
    ('http://Yéti.ORG', 'http://xn--yti-bma.org/', 'xn--yti-bma.org'),
    ('http://xn--yti-bma.org', 'http://xn--yti-bma.org/', 'xn--yti-bma.org'),
)

FAILING_TESTS = (
    ('http://ye ti.org'),
    ('http://----.com'),
    ('http://ye_ti.org'),
)

@pytest.mark.usefixtures('clean_db')
def test_url_idna():
    """Tests that a URL's value and IDNA are correctly normalized."""
    for value, expected, _ in NORMALIZATION_TESTS:
        obs = URL(value=value)
        obs.normalize()
        assert obs.value == expected

@pytest.mark.usefixtures('clean_db')
def test_url_fails():
    """Test that invalid urls cannot be created."""
    for failing_value in FAILING_TESTS:
        with pytest.raises(ValidationError):
            URL(value=failing_value)
