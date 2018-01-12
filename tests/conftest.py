import pytest

from yeti.common.config import yeti_config
from yeti.core.model.arango import db

# Make sure we are not deleting the user's database when running tests
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'


@pytest.fixture
def clean_db():
    db.clear()
