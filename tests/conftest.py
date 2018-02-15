import pytest

from yeti.common.config import yeti_config
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

# pylint: disable=wrong-import-position
from yeti.core.model.arango import db
from yeti.core.types.observable import Observable
from yeti.core.types.hostname import Hostname
from yeti.core.types.tag import Tag

# Make sure we are not deleting the user's database when running tests

@pytest.fixture
def clean_db():
    # pylint: disable=protected-access
    # We need to access the collections to make sure they are in the cache
    Observable._get_collection()
    Hostname._get_collection()
    Tag._get_collection()
    db.clear()


@pytest.fixture
def populated_db():
    db.clear()
    observables = []
    for num in range(10):
        obs = Observable.get_or_create(value='asd{0:d}'.format(num))
        hostname = Hostname.get_or_create(value='asd{0:d}.com'.format(num))
        observables.extend([obs, hostname])
    return observables
