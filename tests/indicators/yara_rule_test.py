"""Tests for the Yara rule datatype."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.indicators.yara_rule import YaraRule

@pytest.mark.usefixtures('clean_db', 'populate_yara_rules')
def test_get_yara_rule():
    """Tests that a YaraRule fetched from the DB has the correct type."""
    yr = YaraRule.filter({'name': 'MZ'})[0]
    assert isinstance(yr, YaraRule)

@pytest.mark.usefixtures('clean_db')
def test_yara_rule_get_or_create(populate_yara_rules):
    """Tests the creation of a single Yara rule."""
    test_rule = populate_yara_rules[0].pattern
    yr = YaraRule.get_or_create(name='other_rule', pattern=test_rule)
    assert isinstance(yr, YaraRule)
    assert yr.id is not None

@pytest.mark.usefixtures('clean_db', 'populate_yara_rules')
def test_yara_rule_attributes():
    """Tests that a created YaraRule has all needed attributes."""
    for rule in YaraRule.list():
        assert isinstance(rule.pattern, str)
        assert hasattr(rule, 'compiled_rule')

@pytest.mark.usefixtures('clean_db')
def test_invalid_yara_rule(populate_yara_rules):
    """Tests that Yara rule can't be created with invalid names or patterns."""
    with pytest.raises(ValidationError):
        YaraRule(name="FailRule", pattern=123).save()
    with pytest.raises(ValidationError):
        test_rule = populate_yara_rules[0].pattern
        YaraRule(name="FailRule", pattern=test_rule[:-1]).save()

MATCHING_TEST = [
    (b'MZ\x00\x00\x00\x00\x00\x00\x00', {
        'name': 'MZ',
        'details': [{'bytes': {'b64': "b'TVo='"}, 'name': '$MZ', 'offset': 0}],
    }),
    (b'PK\x00\x00\x00\x00\x00\x00\x00', None),
]

@pytest.mark.usefixtures('clean_db')
def test_yara_rule_match(populate_yara_rules):
    r = populate_yara_rules[0]
    for test, expected in MATCHING_TEST:
        assert r.match(test) == expected
