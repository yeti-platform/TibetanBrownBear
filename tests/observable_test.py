import unittest

from yeti.core.types.observable import Observable
from yeti.core.model.arango import ArangoYetiConnector
import logging

class TestObservables(unittest.TestCase):

    def setUp(self):
        ArangoYetiConnector.clear_db()

    def test_observable_creation(self):
        obs = Observable(value='asd')
        self.assertIsNone(obs.key)
        obs = obs.save()
        print(obs.dump(), obs.key)
        self.assertIsNotNone(obs.key)

    def test_observable_fetch(self):
        obs = Observable(value='asd').save()
        key = obs.key
        fetched_obs = Observable.get(key)
        self.assertEqual(fetched_obs.key, key)
