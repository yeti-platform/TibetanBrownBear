"""Detail Yeti's IP object structure."""
import re

import ipaddress

from stix2 import IPv4Address as STIXIPv4Address

from yeti.core.helpers import refang
from .observable import Observable

class IP(Observable):  # pylint: disable=too-many-ancestors
    """IP Yeti object.

    Attributes:
      geoip: Geographical IP information, when available.
      version: The IP version (4 or 6).
    """

    type = 'ipv4-addr'
    _strip_leading_zeros = re.compile(r'(^|:|\.)0+(?=[^.])')

    @classmethod
    def validate_string(cls, string):
        string = cls._strip_leading_zeros.sub(r'\1', string)
        try:
            ipaddress.ip_address(string)
            return True
        except ValueError:
            return False

    def normalize(self):
        """Normalize the IP address."""
        value = self._strip_leading_zeros.sub(r'\1', self.value)
        value = str(ipaddress.ip_address(value))
        self._stix_object = STIXIPv4Address(value=value)

Observable.datatypes[IP.type] = IP
