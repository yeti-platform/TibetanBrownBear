"""Detail Yeti's URL object structure."""

import re
from urllib.parse import urlparse

from marshmallow import fields
from url_normalize import url_normalize

from yeti.core.helpers import refang
from .observable import Observable, ObservableSchema
from . import hostname
from . import ip

# pylint: disable=line-too-long
MAIN_REGEX = r'(?P<search>((?P<scheme>[\w]{2,9}):\/\/)?([\S]*\:[\S]*\@)?(?P<host>[-.\w]+)(\:[\d]{1,5})?(?P<path>(\/[\S]*)?(\?[\S]*)?(\#[\S]*)?))'
FULL_REGEX = r'(?P<search>((?P<scheme>[\w]{2,9}):\/\/)?([\S]*\:[\S]*\@)?(?P<host>[-.\w]+)(\:[\d]{1,5})?(?P<path>((\/[\S]*)?(\?[\S]*)?(\#[\S]*)?)[\w/])?)'
PREFIX_REGEX = r'[^:]+://'

COMPILED_MAIN = re.compile(MAIN_REGEX)
COMPILED_FULL_REGEX = re.compile(FULL_REGEX)
COMPILED_PREFIX_REGEX = re.compile(PREFIX_REGEX)

class URLSchema(ObservableSchema):
    """(De)serialization marshmallow.Schema for Url objects."""
    parsed = fields.Dict()
    type = fields.String()

class URL(Observable):
    """URL Yeti object.

    Attributes:
      tld: The corresponding TLD.
    """

    schema = URLSchema
    _collection_name = 'observables'

    type = 'observable.url'
    parsed = {}

    @classmethod
    def validate_string(cls, string):
        match = COMPILED_FULL_REGEX.match(refang(string))
        if match and ((match.group('search').find('/') != -1) and (
                hostname.Hostname.validate_string(match.group('host')) or
                ip.IP.validate_string(match.group('host')))):
            return True
        return False

    def normalize(self):
        self.value = refang(self.value).lower()

        if COMPILED_PREFIX_REGEX.match(self.value) is None:
            # if no schema is specified, assume http://
            self.value = 'http://' + self.value

        # NOTE: url_normalize converts the URL to IDNA, it would be nice to also
        # keep the encoded URL
        self.value = url_normalize(self.value)
        self.parse()

    def parse(self):
        parsed = urlparse(self.value)

        self.parsed = {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc.split(":")[0],
            "port": parsed.port,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment
        }

Observable.datatypes[URL.type] = URL
