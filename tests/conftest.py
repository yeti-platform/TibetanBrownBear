# pylint: disable=wrong-import-position

import pytest

from yeti.common.config import yeti_config
# Make sure we are not deleting the user's database when running tests
yeti_config.arangodb.database = yeti_config.arangodb.database + '__tests'

from yeti.core.model.arango import db

from yeti.core.relationships import Relationship

from yeti.core.entities.entity import Entity
from yeti.core.entities.malware import Malware

from yeti.core.indicators.indicator import Indicator
from yeti.core.indicators.regex import Regex
from yeti.core.indicators.yara import Yara

from yeti.core.observables.observable import Observable
from yeti.core.observables.hostname import Hostname
from yeti.core.observables.url import URL
from yeti.core.observables.ip import IP
from yeti.core.observables.tag import Tag

# Async jobs
from yeti.core import async

# Settings
from yeti.core.model.settings.vocabs import Vocabs


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
    Indicator._get_collection()
    Malware._get_collection()
    Observable._get_collection()
    Hostname._get_collection()
    Tag._get_collection()
    Vocabs._get_collection()
    Relationship._get_collection()
    db.delete_graph('stix')
    db.delete_graph('tags')
    db.clear()

@pytest.fixture
def populate_settings():
    vocabs = Vocabs().save()
    vocabs.set_vocab('malware-label-ov', sorted([
        'adware',
        'backdoor'
    ]))
    return [vocabs]

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
    m3 = Malware(name='Zeus', labels=['trojan']).save()
    malware.append(m3)
    return malware

@pytest.fixture
def populate_regex():
    r1 = Regex(
        name='Zeus C2',
        labels=['malicious-activity'],
        description='This is how C2 URLs for Zeus usually end.',
        pattern=r'gate\.php$',
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[
            {
                'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
                'phase_name': 'reconnaissance'
            }
        ]
    ).save()

    r2 = Regex(
        name='AppData',
        labels=['persistence'],
        description='AppData directory',
        pattern=r'Roaming\\AppData\\\w+$',
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[
            {
                'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
                'phase_name': 'reconnaissance'
            }
        ]
    ).save()

    return [r1, r2]


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
    y = Yara(
        name='MZ',
        labels=['binary-data'],
        description='This is how PEs usually start with.',
        pattern=TEST_RULE,
        valid_from='2016-01-01T00:00:00Z',
        valid_until='2017-01-01T00:00:00Z',
        kill_chain_phases=[
            {
                'kill_chain_name': 'lockheed-martin-cyber-kill-chain',
                'phase_name': 'reconnaissance'
            }
        ]
    ).save()
    return [y]

@pytest.fixture
def populate_all():
    clean_db()
    populate_hostnames()
    populate_urls()
    populate_ips()
    populate_malware()
    populate_regex()
    populate_yara_rules()
