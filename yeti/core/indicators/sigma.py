import yaml
from sigma.parser.collection import SigmaCollectionParser
from sigma.parser.exceptions import SigmaParseError, SigmaCollectionParseError
from stix2 import CustomObject, KillChainPhase, properties

from yeti.core.errors import ValidationError

from .indicator_base import Indicator


@CustomObject('x-sigma', [
    ('labels', properties.StringProperty(required=True)),
    ('name', properties.StringProperty()),
    ('description', properties.StringProperty()),
    ('pattern', properties.StringProperty(required=True)),
    ('valid_from', properties.TimestampProperty(required=True)),
    ('valid_until', properties.TimestampProperty()),
    ('kill_chain_phases', properties.ListProperty(KillChainPhase))
])
class StixSigma():
    def __init__(self, pattern=None, **_):
        try:
            SigmaCollectionParser(self.pattern)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
            raise ValidationError('{0:s} is not a valid YAML markup: {1!s}'.format(pattern, e))
        except (SigmaParseError, SigmaCollectionParseError) as e:
            raise ValidationError('{0:s} is not a valid Sigma rule: {1!s}'.format(pattern, e))


class Sigma(Indicator):
    """Sigma rule STIX extension object.

    Extends the Indicator STIX2 definition.
    """

    type = 'x-sigma'

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

Indicator.datatypes[Sigma.type] = Sigma
