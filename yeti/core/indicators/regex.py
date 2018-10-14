import re

from stix2 import CustomObject, properties, KillChainPhase

from .indicator_base import Indicator
from yeti.core.errors import ValidationError

@CustomObject('x-regex', [
    ('labels', properties.StringProperty(required=True)),
    ('name', properties.StringProperty()),
    ('description', properties.StringProperty()),
    ('pattern', properties.StringProperty(required=True)),
    ('valid_from', properties.TimestampProperty(required=True)),
    ('valid_until', properties.TimestampProperty()),
    ('kill_chain_phases', properties.ListProperty(KillChainPhase))
])
class StixRegex():
    def __init__(self, pattern=None, **_):
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValidationError('{0:s} is not a valid regular expression: {1:s}'.format(pattern, str(e)))


class Regex(Indicator):
    """STIX Indicator Yeti object.

    Extends the Indicator STIX2 definition.
    """

    _collection_name = 'indicators'
    type = 'x-regex'

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
    def kill_chain_pahses(self):
        return self._stix_object.kill_chain_pahses

Indicator.datatypes[Regex.type] = Regex
