"""Tests for the regex datatype."""
import re

import pytest

from yeti.core.errors import ValidationError
from yeti.core.indicators.regex import Regex

@pytest.mark.usefixtures('clean_db')
def test_get_regex(populate_regex):
    """Tests that a YaraRule fetched from the DB has the correct type."""
    name = populate_regex[0].name
    yr = Regex.filter({'name': name})[0]
    assert isinstance(yr, Regex)

@pytest.mark.usefixtures('clean_db')
def test_regex_get_or_create(populate_regex):
    """Tests the creation of a single regex."""
    test_pattern = populate_regex[0].pattern
    regex = Regex.get_or_create(name='random', pattern=test_pattern)
    assert isinstance(regex, Regex)
    assert regex.id is not None
    assert regex.pattern == test_pattern

@pytest.mark.usefixtures('clean_db', 'populate_regex')
def test_yara_rule_attributes():
    """Tests that a created YaraRule has all needed attributes."""
    regex_type = type(re.compile(''))
    for rule in Regex.list():
        assert isinstance(rule.pattern, str)
        assert hasattr(rule, 'compiled_regex')
        assert isinstance(rule.compiled_regex, regex_type)

@pytest.mark.usefixtures('clean_db')
def test_invalid_yara_rule():
    """Tests that regex can't be created with invalid names or patterns."""
    with pytest.raises(ValidationError):
        Regex(name="FailRule", pattern=123).save()
    with pytest.raises(ValidationError):
        Regex(name="FailRule", pattern='asd[3-2]').save()

MATCHING_TEST = (
    ('C\\Users\\tomchop\\AppData\\Roaming\\Google', {
        'name': 'AppData',
        'details': 'AppData\\Roaming\\Google'
    }),
    ('C\\Users\\tomchop\\AppData\\Local\\Google', None),
)

@pytest.mark.usefixtures('clean_db')
def test_regex_match(populate_regex):
    r = populate_regex[0]
    for test, expected in MATCHING_TEST:
        assert r.match(test) == expected
