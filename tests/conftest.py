import pytest

from yeti.common.config import yeti_config
from yeti.core.model.arango import db
from yeti.core.types.observable import Observable

# Make sure we are not deleting the user's database when running tests
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'


@pytest.fixture
def clean_db():
    db.clear()


@pytest.fixture
def populated_db():
    db.clear()
    for num in range(10):
        # We need to control the keys with which objects are created
        # pylint: disable=W0212
        Observable._get_collection().insert({
            'value': 'asd{0:d}'.format(num),
            '_key': str(num),
        })
