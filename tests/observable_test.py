# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

from yeti.core.types.observable import Observable


def test_observable_creation(clean_db):
    """Tests the creation of a single observable."""
    obs = Observable(value='asd')
    assert obs.id is None
    obs = obs.save()
    assert isinstance(obs, Observable)
    assert obs.id is not None


def test_observable_fetch(clean_db):
    """Tests fetching a single observable by id."""
    obs = Observable(value='asd').save()
    fetched_obs = Observable.get(obs.id)
    assert isinstance(fetched_obs, Observable)
    assert fetched_obs.id == obs.id


def test_observables_list(populated_db):
    """Tests fetching all observables in the database."""
    allitems = Observable.list()
    assert isinstance(allitems[0], Observable)
    assert len(allitems) == 10
