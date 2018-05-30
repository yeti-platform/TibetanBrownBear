import pytest

from yeti.common.config import yeti_config
# Make sure we are not deleting the user's database when running tests
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

# pylint: disable=wrong-import-position
from yeti.core.model.arango import db
from yeti.core.indicators.yara_rule import YaraRule
from yeti.core.indicators.regex import Regex
from yeti.core.entities.entity import Entity
from yeti.core.entities.malware import Malware
from yeti.core.observables.observable import Observable
from yeti.core.observables.hostname import Hostname
from yeti.core.observables.url import URL
from yeti.core.observables.ip import IP
from yeti.core.observables.tag import Tag

from yeti.core import async

class DummyFeed1(async.AsyncJob):
    def execute(self):
        return 5

class DummyFeed2(async.AsyncJob):
    def execute(self):
        return 10

async.functions['DummyFeed1'] = DummyFeed1
async.functions['DummyFeed2'] = DummyFeed2

@pytest.fixture
def populate_feeds():
    return [
        DummyFeed1(),
        DummyFeed2()
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
    YaraRule._get_collection()
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
def populate_entities():
    entities = []
    for num in range(10):
        entity = Entity.get_or_create(name='entity{0:d}'.format(num))
        entities.append(entity)
    return entities

@pytest.fixture
def populate_malware():
    m1 = Malware(name='Gootkit').save()
    m1.family = ['banker', 'trojan']
    m1.save()
    m2 = Malware(name='Sofacy').save()
    m2.family = ['trojan']
    m2.save()
    return [m1, m2]

TEST_RULE = """rule yeti_rule
{
    meta:
        description = "Test rule"

    strings:
        $MZ = { 4D 5A }

    condition:
        $MZ
}"""

@pytest.fixture
def populate_yara_rules():
    y1 = YaraRule(name='MZ', pattern=TEST_RULE).save()
    return [y1]

@pytest.fixture
def populate_regex():
    r = Regex(name='AppData', pattern=r'AppData\\Roaming\\\w+').save()
    return [r]

@pytest.fixture
def populate_all():
    clean_db()
    populate_hostnames()
    populate_malware()
    populate_yara_rules()
