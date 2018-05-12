"""Detail Yeti's IP object structure."""

import ipaddress

from marshmallow import fields

from yeti.core.helpers import refang
from .observable import Observable, ObservableSchema

class IPSchema(ObservableSchema):
    """(De)serialization marshmallow.Schema for IP objects."""
    geoip = fields.Dict(allow_none=True)
    version = fields.Int(allow_none=True)
    type = fields.String()

class IP(Observable):
    """IP Yeti object.

    Attributes:
      geoip: Geographical IP information, when available.
      version: The IP version (4 or 6).
    """

    schema = IPSchema
    _collection_name = 'observables'

    type = 'observable.ip'
    geoip = None
    version = None

    @classmethod
    def validate_string(cls, string):
        string = refang(string)
        try:
            ipaddress.ip_address(string)
            return True
        except ValueError:
            return False

    def normalize(self):
        self.value = refang(self.value)
        ipaddr_object = ipaddress.ip_address(self.value)
        self.value = str(ipaddr_object)
        self.version = ipaddr_object.version

Observable.datatypes[IP.type] = IP
