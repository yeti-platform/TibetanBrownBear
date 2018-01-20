"""Detail the Yeti's Observable object structure."""

import re

import idna
from marshmallow import fields
from tldextract import extract
from marshmallow import fields, post_load


from yeti.core.helpers import refang
from .observable import Observable, ObservableSchema

MAIN_REGEX = r'[-.\w[\]]+\[?\.\]?[\w]+'
FULL_REGEX = r'(?P<pre>\W?)(?P<search>' + MAIN_REGEX + r')(?P<post>\W?)'
COMPILED_MAIN = re.compile(MAIN_REGEX)
COMPILED_FULL_REGEX = re.compile(FULL_REGEX)

class HostnameSchema(ObservableSchema):
    """(De)serialization marshmallow.Schema for Hostname objects."""
    tld = fields.String(allow_none=True)
    idna = fields.String(allow_none=True)
    type = fields.Constant("hostname")

class Hostname(Observable):
    """Observable Yeti object.

    Attributes:
      tld: The corresponding TLD.
    """

    _schema = HostnameSchema
    _collection_name = 'hostnames'

    tld = None
    idna = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tld = kwargs.get('tld')

    @classmethod
    def is_valid(cls, text):
        match = COMPILED_FULL_REGEX.match(text)
        if not match:
            return False

        if match.group('pre') != '/' and match.group('post') != '/':
            value = refang(match.group('search'))
            if len(value) <= 255:
                parts = extract(value)
                if parts.suffix and parts.domain:
                    return True

        return False

    def normalize(self):
        self.value = refang(self.value.lower())
        if self.value.endswith("."):
            self.value = self.value[:-1]

        try:
            self.idna = idna.encode(self.value)
        except idna.core.InvalidCodepoint:
            pass


HostnameSchema.constructor = Hostname
