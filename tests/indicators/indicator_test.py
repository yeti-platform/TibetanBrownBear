"""Tests for the Malware datatype."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.indicators.indicator import Indicator

@pytest.mark.usefixtures('clean_db')
def test_invalid_indicator_name():
    """Tests that an indicator with an invalid name cannot be created."""
    with pytest.raises(ValidationError):
        Indicator(name=123).save()

@pytest.mark.usefixtures('clean_db', 'populate_entities')
def test_indicator_formatting():
    """Tests correct indicator formatting to string."""
    ent = Indicator(name='asd').save()
    assert str(ent) == "<Indicator('asd')>"
