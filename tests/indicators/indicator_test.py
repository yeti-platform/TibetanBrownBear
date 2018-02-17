# pylint: disable=unused-argument
"""Tests for the Malware datatype."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.indicators.indicator import Indicator

def test_invalid_indicator_name(clean_db):
    """Tests that an indicator with an invalid name cannot be created."""
    with pytest.raises(ValidationError):
        Indicator(name=123).save()

def test_indicator_formatting(clean_db, populate_entities):
    """Tests correct indicator formatting to string."""
    ent = Indicator(name='asd').save()
    assert str(ent) == "<Indicator(name='asd')>"
