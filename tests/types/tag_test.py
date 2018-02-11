# pylint: disable=unused-argument
import pytest

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from yeti.core.types.tag import Tag

def test_tag_observable(populated_db):
    """Tests that tagging is committed to the database."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    fetched_obs = Observable.get(obs.id)
    assert fetched_obs.tags != []

def test_tag_creation(clean_db):
    """Tests that a Tag object can be created."""
    tag = Tag(name='yeti').save()
    assert tag is not None

def test_tag_creation_on_tag(clean_db):
    """Tests that tagging an observable creates a Tag object."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    tag_name = obs.tags[0].name
    assert len(Tag.filter({'name': tag_name})) == 1

def test_tagref_creation(clean_db):
    obs = Observable.get_or_create(value='asd')
    obs.tag('yeti')
    obs = Observable.get_or_create(value='asd')
    assert obs.tags[0].name == 'yeti'

def test_tag_count_update(clean_db):
    """Tests that tagging an observable increases the global tag number."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    assert Tag.get_or_create(name='yeti').count == 1

def test_invalid_tag_name(clean_db):
    """Tests for invalid tag names."""
    with pytest.raises(ValidationError):
        Tag(name='!@#$%^&*()').save()

def test_tag_formatting(clean_db):
    """Tests that tags are formatted correctly when printed."""
    tag = Tag(name='yeti').save()
    assert str(tag) == "<Tag('yeti')>"
