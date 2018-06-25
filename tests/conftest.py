import pytest

from yeti.common.config import yeti_config
# Make sure we are not deleting the user's database when running tests
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

# pylint: disable=wrong-import-position
from yeti.core.model.arango import db
from yeti.core.entities.entity import Entity
from yeti.core.entities.malware import Malware
from yeti.core.observables.observable import Observable
from yeti.core.observables.hostname import Hostname
from yeti.core.observables.url import URL
from yeti.core.observables.ip import IP
from yeti.core.observables.tag import Tag

from yeti.core import async

class FastDummyFeed(async.AsyncJob):
    def execute(self):
        return 5

class SlowDummyFeed(async.AsyncJob):
    def execute(self):
        import time
        time.sleep(3)
        return 10

async.functions['FastDummyFeed'] = FastDummyFeed
async.functions['SlowDummyFeed'] = SlowDummyFeed

@pytest.fixture
def populate_feeds():
    return [
        FastDummyFeed(),
        SlowDummyFeed()
    ]

@pytest.fixture
def clean_db():
    # pylint: disable=protected-access
    # We need to access the collections to make sure they are in the cache
    Entity._get_collection()
    Malware._get_collection()
    Observable._get_collection()
    Hostname._get_collection()
    Tag._get_collection()
    db.clear()


@pytest.fixture
def populate_hostnames():
    hostnames = []
    for num in range(10):
        hostname = Hostname.get_or_create(value='asd{0:d}.com'.format(num))
        hostnames.append(hostname)
    return hostnames

@pytest.fixture
def populate_urls():
    urls = []
    for num in range(10):
        url = URL.get_or_create(value='http://asd{0:d}.com'.format(num))
        urls.append(url)
    return urls

@pytest.fixture
def populate_ips():
    ips = []
    for num in range(10):
        ip = IP.get_or_create(value='127.0.0.{0:d}'.format(num))
        ips.append(ip)
    return ips

@pytest.fixture
def populate_malware():
    malware = []
    m1 = Malware(name='Gootkit', labels=['banker']).save()
    malware.append(m1)
    m2 = Malware(name='Sofacy', labels=['apt']).save()
    malware.append(m2)
    return malware

@pytest.fixture
def populate_all():
    clean_db()
    populate_hostnames()
    populate_malware()
