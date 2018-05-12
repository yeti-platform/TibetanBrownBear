"""Detail Yeti's Hostname object structure."""

import re

import idna
from marshmallow import fields
from tldextract import extract

from yeti.core.helpers import refang
from .observable import Observable, ObservableSchema

MAIN_REGEX = r'([-.\w]+)?[^-]\[?\.\]?[a-z]+'
FULL_REGEX = r'(?P<pre>\W?)(?P<search>' + MAIN_REGEX + r')(?P<post>\W?)'
COMPILED_MAIN = re.compile(MAIN_REGEX, flags=re.IGNORECASE)
COMPILED_FULL_REGEX = re.compile(FULL_REGEX, flags=re.IGNORECASE)

class HostnameSchema(ObservableSchema):
    """(De)serialization marshmallow.Schema for Hostname objects."""
    tld = fields.String(allow_none=True)
    idna = fields.String(allow_none=True)
    type = fields.String()

class Hostname(Observable):
    """Observable Yeti object.

    Attributes:
      tld: The corresponding TLD.
    """

    schema = HostnameSchema
    _collection_name = 'observables'

    type = 'observable.hostname'
    idna = None

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
        self.value = refang(self.value.lower())
        if self.value.endswith('.'):
            self.value = self.value[:-1]

        self.value = idna.decode(self.value)
        self.idna = idna.encode(self.value)

Observable.datatypes[Hostname.type] = Hostname
