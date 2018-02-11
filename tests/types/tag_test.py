# pylint: disable=unused-argument
import pytest

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from yeti.core.types.tag import Tag

def test_tagref_creation(clean_db):
    """Tests that tagging is committed to the database."""
    obs = Observable.get_or_create(value='asd')
    obs.tag('yeti')
    obs = Observable.get_or_create(value='asd')
    assert obs.tags[0].name == 'yeti'

def test_tag_creation(clean_db):
    """Tests that a Tag object can be created."""
    tag = Tag(name='yeti').save()
    assert tag is not None

def test_tag_creation_on_tag(clean_db):
    """Tests that tagging an observable creates a unique Tag object."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    obs = Observable(value='dsa').save()
    obs.tag('yeti')
    tag_name = obs.tags[0].name
    assert len(Tag.filter({'name': tag_name})) == 1

def test_tag_count_update(clean_db):
    """Tests that tagging an observable increases the global tag number."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    assert Tag.get_or_create(name='yeti').count == 1

def test_invalid_tag_name(clean_db):
    """Tests that tags with invalid names can't be created."""
    with pytest.raises(ValidationError):
        Tag(name='!@#$%^&*()').save()

def test_last_seen(clean_db):
    """Tests that last_seen timestmaps are updated."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    obs = Observable.get_or_create(value='asd')
    obs.tag('yeti')
    obs = Observable.get_or_create(value='asd')
    assert obs.tags[0].first_seen < obs.tags[0].last_seen

def test_unique_tagref(clean_db):
    """Tests that tagrefs are unique per observable."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    obs.tag('yeti')
    assert len(obs.tags) == 1

def test_tag_formatting(clean_db):
    """Tests that tags are formatted correctly when printed."""
    tag = Tag(name='yeti').save()
    assert str(tag) == "<Tag('yeti')>"

def test_tagref_formatting(clean_db):
    """Tests that tags are formatted correctly when printed."""
    obs = Observable(value='asd').save()
    obs.tag('yeti')
    assert str(obs.tags[0]) == "<TagRef('yeti')>"
