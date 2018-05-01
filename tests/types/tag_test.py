"""Tests for tagging functionality."""
import pytest

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from yeti.core.types.tag import Tag

@pytest.mark.usefixtures('clean_db')
def test_tagref_creation():
    """Tests that tagging is committed to the database."""
    obs = Observable.get_or_create(value='asd')
    obs.tag(['yeti'])
    obs = Observable.get_or_create(value='asd')
    assert obs.tags[0].name == 'yeti'

@pytest.mark.usefixtures('clean_db')
def test_tag_creation():
    """Tests that a Tag object can be created."""
    tag = Tag(name='yeti').save()
    assert tag is not None

@pytest.mark.usefixtures('clean_db')
def test_tag_creation_on_tag():
    """Tests that tagging an observable creates a unique Tag object."""
    obs = Observable(value='asd').save()
    obs.tag(['yeti'])
    obs = Observable(value='dsa').save()
    obs.tag(['yeti'])
    tag_name = obs.tags[0].name
    assert len(Tag.filter({'name': tag_name})) == 1

@pytest.mark.usefixtures('clean_db')
def test_invalid_tag_name():
    """Tests that tags with invalid names can't be created."""
    with pytest.raises(ValidationError):
        Tag(name='!@#$%^&*()').save()

@pytest.mark.usefixtures('clean_db')
def test_last_seen():
    """Tests that last_seen timestmaps are updated."""
    obs = Observable(value='asd').save()
    obs.tag(['yeti'])
    obs = Observable.get_or_create(value='asd')
    obs.tag(['yeti'])
    obs = Observable.get_or_create(value='asd')
    assert obs.tags[0].first_seen < obs.tags[0].last_seen

@pytest.mark.usefixtures('clean_db')
def test_unique_tagref():
    """Tests that tagrefs are unique per observable."""
    obs = Observable(value='asd').save()
    obs.tag(['yeti'])
    obs.tag(['yeti'])
    assert len(obs.tags) == 1

@pytest.mark.usefixtures('clean_db')
def test_multiple_tags():
    """Tests that tagrefs are unique per observable."""
    obs = Observable(value='asd').save()
    test_tags = ['asd', 'dsa', 'zxc', 'cxz']
    obs.tag(test_tags)
    assert len(obs.tags) == 4

@pytest.mark.usefixtures('clean_db')
def test_tag_formatting():
    """Tests that tags are formatted correctly when printed."""
    tag = Tag(name='yeti').save()
    assert str(tag) == "<Tag('yeti')>"

@pytest.mark.usefixtures('clean_db')
def test_tagref_formatting():
    """Tests that tags are formatted correctly when printed."""
    obs = Observable(value='asd').save()
    obs.tag(['yeti'])
    assert str(obs.tags[0]) == "<TagRef('yeti')>"

@pytest.mark.usefixtures('clean_db')
def test_strict_tagging():
    """Tests that tags are formatted correctly when printed."""
    obs = Observable(value='asd').save()
    obs.tag(['yeti'])
    obs.tag(['yeti2'], strict=True)
    assert len(obs.tags) == 1
    assert obs.tags[0].name == 'yeti2'
