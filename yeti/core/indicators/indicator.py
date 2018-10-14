"""Detail Yeti's Indicator object structure."""

from .indicator_base import Indicator

class STIXIndicator(Indicator):
    """STIX Indicator Yeti object.

    Extends the Indicator STIX2 definition.
    """

    type = 'indicator'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def pattern(self):
        return self._stix_object.pattern

    @property
    def valid_from(self):
        return self._stix_object.valid_from

    @property
    def valid_until(self):
        return self._stix_object.valid_until

    @property
    def kill_chain_phases(self):
        return self._stix_object.kill_chain_phases

Indicator.datatypes[STIXIndicator.type] = STIXIndicator
