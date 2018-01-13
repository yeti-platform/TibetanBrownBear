# pylint: disable=unused-argument
"""Tests for the Observable datatype."""

from yeti.core.types.observable import Observable


def test_observable_creation():
    """Tests the creation of a single observable."""
    obs = Observable(value='asd')
    assert obs.key is None
    obs = obs.save()
    assert isinstance(obs, Observable)
    assert obs.key is not None


def test_observable_fetch():
    """Tests fetching a single observable by key."""
    obs = Observable(value='asd').save()
    key = obs.key
    fetched_obs = Observable.get(key)
    assert isinstance(fetched_obs, Observable)
    assert fetched_obs.key == key


def test_observables_list(clean_db):
    """Tests fetching all observables in the database."""
    for num in range(10):
        Observable(value='asd{0:d}'.format(num)).save()
    allitems = Observable.list()
    assert isinstance(allitems[0], Observable)
    assert len(allitems) == 10
