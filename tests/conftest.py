import pytest

from yeti.common.config import yeti_config
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

# pylint: disable=wrong-import-position
from yeti.core.model.arango import db
from yeti.core.types.observable import Observable
from yeti.core.types.hostname import Hostname

# Make sure we are not deleting the user's database when running tests

@pytest.fixture
def clean_db():
    # pylint: disable=protected-access
    # We need to access the collections to make sure they are in the cache
    Observable._get_collection()
    Hostname._get_collection()
    db.clear()


@pytest.fixture
def populated_db():
    db.clear()
    for num in range(10):
        # We need to control the keys with which objects are created
        # pylint: disable=protected-access
        Observable._get_collection().insert({
            'value': 'asd{0:d}'.format(num),
            '_key': str(num),
            'type': 'observable',
        })
        Hostname._get_collection().insert({
            'value': 'asd{0:d}.com'.format(num),
            '_key': str(num+10),
            'tld': 'com',
            'type': 'observable.hostname',
            'idna': 'asd{0:d}.com'.format(num),
        })
