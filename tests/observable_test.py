"""Tests for the Observable datatype."""

import unittest

from yeti.core.types.observable import Observable
from yeti.core.model.arango import ArangoYetiConnector

class TestObservables(unittest.TestCase):
    """Tests for the Observable datatype."""

    def setUp(self):
        ArangoYetiConnector.clear_db()

    def test_observable_creation(self):
        """Tests the creation of a single observable."""
        obs = Observable(value='asd')
        self.assertIsNone(obs.key)
        obs = obs.save()
        self.assertIsInstance(obs, Observable)
        self.assertIsNotNone(obs.key)

    def test_observable_fetch(self):
        """Tests fetching a single observable by key."""
        obs = Observable(value='asd').save()
        key = obs.key
        fetched_obs = Observable.get(key)
        self.assertIsInstance(fetched_obs, Observable)
        self.assertEqual(fetched_obs.key, key)

    def test_observables_list(self):
        """Tests fetching all observables in the database."""
        for num in range(10):
            Observable(value='asd{0:d}'.format(num)).save()
        allitems = Observable.list()
        self.assertIsInstance(allitems[0], Observable)
        self.assertEqual(len(allitems), 10)
