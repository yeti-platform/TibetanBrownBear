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
    _strip_leading_zeros = re.compile(r'\.0{2,}')

    @classmethod
    def validate_string(cls, string):
        string = '.'.join([str(int(octets)) for octets in refang(string).split('.')])
        try:
            ipaddress.ip_address(string)
            return True
        except ValueError:
            return False

    def normalize(self):
        """Normalize the IP address."""
        final = '.'.join([str(int(octets)) for octets in refang(self.value).split('.')])
        value = str(ipaddress.ip_address(final))
        self._stix_object = STIXIPv4Address(value=value)

Observable.datatypes[IP.type] = IP
