import pytest

from yeti.core import helpers


REFANG_TESTS = [
    ('hxxp://yeti.org/', 'http://yeti.org/'),
    ('me0w://yeti.org/', 'http://yeti.org/'),
    ('http://www[.]yeti[.]org/', 'http://www.yeti.org/'),
    ('yeti[.]org', 'yeti.org'),
    ('www[.]yeti[.]org', 'www.yeti.org'),
    ('127[.]0[.]0[.]1', '127.0.0.1'),
]

@pytest.mark.usefixtures('clean_db')
def test_refang():
    """Tests refanging URLs, Hostnames, and IPs"""
    for test, expected in REFANG_TESTS:
        assert helpers.refang(test) == expected
