"""Detail Yeti's IP object structure."""

import ipaddress

from stix2 import IPv4Address as STIXIPv4Address

from yeti.core.helpers import refang
from .observable import Observable

class IP(Observable):
    """IP Yeti object.

    Attributes:
      geoip: Geographical IP information, when available.
      version: The IP version (4 or 6).
    """

    type = 'ipv4-addr'

    @classmethod
    def validate_string(cls, string):
        string = refang(string)
        try:
            ipaddress.ip_address(string)
            return True
        except ValueError:
            return False

    def normalize(self):
        value = refang(self._stix_object.value)
        ipaddr_object = ipaddress.ip_address(value)
        value = str(ipaddr_object)
        self._stix_object = STIXIPv4Address(value=value)

Observable.datatypes[IP.type] = IP
