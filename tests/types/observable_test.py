# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from yeti.core.types.hostname import Hostname


def test_observable_creation(clean_db):
    """Tests the creation of a single observable."""
    obs = Observable(value='asd')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Observable)
    assert obs.id is not None


def test_observable_get(clean_db):
    """Tests fetching a single observable by id."""
    obs = Observable(value='asd').save()
    fetched_obs = Observable.get(obs.id)
    assert isinstance(fetched_obs, Observable)
    assert fetched_obs.id == obs.id

def test_observable_get_or_create(populated_db):
    """Tests the get_or_create function on observables."""
    count = len(Observable.list())
    first_object = Observable.get_or_create(value='asd0')
    second_object = Observable.get_or_create(value='asd0')
    assert count == len(Observable.list())
    assert first_object.id == second_object.id
    Observable.get_or_create(value='asd999')
    assert count + 1 == len(Observable.list())

def test_observables_list(populated_db):
    """Tests fetching all observables in the database."""
    allitems = Observable.list()
    assert isinstance(allitems[0], Observable)
    assert len(allitems) == 20

def test_different_observable_types(populated_db):
    allitems = Observable.list()
    hostname_count = 0
    observable_count = 0
    for item in allitems:
        if isinstance(item, Hostname):
            hostname_count += 1
        elif isinstance(item, Observable):
            observable_count += 1
    assert observable_count == 10
    assert hostname_count == 10

def test_empty_value(clean_db):
    """Tests that an observable with an empty value can't be created."""
    with pytest.raises(ValidationError):
        Observable(value=None)

def test_observable_formatting(clean_db):
    obs = Observable(value='asd').save()
    assert str(obs) == "<Observable(value='asd')>"
