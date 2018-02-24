# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from yeti.core.types.hostname import Hostname


@pytest.mark.usefixtures('clean_db')
def test_observable_creation():
    """Tests the creation of a single observable."""
    obs = Observable(value='asd.com')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Observable)
    assert obs.id is not None

@pytest.mark.usefixtures('clean_db')
def test_observable_get():
    """Tests fetching a single observable by id."""
    obs = Hostname(value='asd.com').save()
    fetched_obs = Observable.get(obs.id)
    assert isinstance(fetched_obs, Observable)
    assert fetched_obs.id == obs.id

@pytest.mark.usefixtures('clean_db', 'populate_hostnames')
def test_observable_get_or_create():
    """Tests the get_or_create function on observables."""
    count = len(Observable.list())
    first_object = Hostname.get_or_create(value='asd0.com')
    second_object = Hostname.get_or_create(value='asd0.com')
    assert count == len(Observable.list())
    assert first_object.id == second_object.id
    Hostname.get_or_create(value='asd999.com')
    assert count + 1 == len(Observable.list())

@pytest.mark.usefixtures('clean_db')
def test_observables_list(populate_hostnames):
    """Tests fetching all observables in the database."""
    allitems = Observable.list()
    assert isinstance(allitems[0], Observable)
    assert len(allitems) == len(populate_hostnames)

@pytest.mark.usefixtures('clean_db')
def test_empty_value():
    """Tests that an observable with an empty value can't be created."""
    with pytest.raises(ValidationError):
        Observable(value=None)
