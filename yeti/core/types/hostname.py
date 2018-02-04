"""Detail the Yeti's Observable object structure."""

import re

import idna
from marshmallow import fields
from tldextract import extract

from yeti.core.helpers import refang
from yeti.core.errors import ValidationError
from .observable import Observable, ObservableSchema
from .observable import DATATYPES

MAIN_REGEX = r'[-.\w[\]]+\[?\.\]?[\w]+'
FULL_REGEX = r'(?P<pre>\W?)(?P<search>' + MAIN_REGEX + r')(?P<post>\W?)'
COMPILED_MAIN = re.compile(MAIN_REGEX)
COMPILED_FULL_REGEX = re.compile(FULL_REGEX)

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

    _schema = HostnameSchema
    _collection_name = 'observables'

    type = 'observable.hostname'
    idna = None

    def is_valid(self):
        match = COMPILED_FULL_REGEX.match(self.value)
        if not match:
            raise ValidationError

        if match.group('pre') != '/' and match.group('post') != '/':
            value = refang(match.group('search'))
            if len(value) <= 255:
                parts = extract(value)
                if parts.suffix and parts.domain:
                    return True

        raise ValidationError

    def normalize(self):
        self.value = refang(self.value.lower())
        if self.value.endswith("."):
            self.value = self.value[:-1]

        self.value = idna.decode(self.value)
        self.idna = idna.encode(self.value)

DATATYPES['observable.hostname'] = Hostname
HostnameSchema.constructor = Hostname
