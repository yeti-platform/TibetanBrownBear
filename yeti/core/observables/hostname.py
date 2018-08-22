"""Detail Yeti's Hostname object structure."""

import re
import json

import idna
from tldextract import extract
from stix2 import DomainName

from yeti.core.helpers import refang
from .observable import Observable

MAIN_REGEX = r'([-.\w]+)?[^-]\[?\.\]?[a-z]+'
FULL_REGEX = r'(?P<pre>\W?)(?P<search>' + MAIN_REGEX + r')(?P<post>\W?)'
COMPILED_MAIN = re.compile(MAIN_REGEX, flags=re.IGNORECASE)
COMPILED_FULL_REGEX = re.compile(FULL_REGEX, flags=re.IGNORECASE)


class Hostname(Observable):
    """Hostname Yeti object."""

    type = 'domain-name'

    @classmethod
    def validate_string(cls, string):
        match = COMPILED_FULL_REGEX.match(string)
        if match and match.group('pre') != '/' and match.group('post') != '/':
            value = refang(match.group('search'))
            if len(value) <= 255 and '_' not in value:
                parts = extract(value)
                if parts.suffix and parts.domain:
                    return True
        return False

    def normalize(self):
        value = refang(self.value.lower())
        if value.endswith('.'):
            value = value[:-1]
        value = idna.decode(value)
        serialized = json.loads(self._stix_object.serialize())
        serialized['value'] = value
        self._stix_object = DomainName(**serialized)

Observable.datatypes[Hostname.type] = Hostname
