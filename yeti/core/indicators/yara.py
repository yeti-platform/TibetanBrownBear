
import base64

from stix2 import CustomObject, properties, KillChainPhase
import yara

from yeti.core.errors import ValidationError
from .indicator_base import Indicator


@CustomObject('x-yara', [
    ('labels', properties.StringProperty(required=True)),
    ('name', properties.StringProperty()),
    ('description', properties.StringProperty()),
    ('pattern', properties.StringProperty(required=True)),
    ('valid_from', properties.TimestampProperty(required=True)),
    ('valid_until', properties.TimestampProperty()),
    ('kill_chain_phases', properties.ListProperty(KillChainPhase))
])
class StixYara():
    def __init__(self, pattern=None, **_):
        try:
            yara.compile(source=pattern)
        except (yara.SyntaxError, yara.Error) as e:
            raise ValidationError('{0:s} is not a valid Yara rule: {1!s}'.format(pattern, e))


class Yara(Indicator):
    """Yara rule STIX extension object.

    Extends the Indicator STIX2 definition.
    """

    type = 'x-yara'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compiled_pattern = yara.compile(source=self.pattern)

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

    def match(self, obj):
        """Matches a Yara rule against a binary stream.

        Args:
            obj: Binary data to match the Yara rule against.

        Returns:
            The matching strings if found, None otherwise.
        """
        matches = self.compiled_pattern.match(data=obj)
        if matches:
            result = {'name': self.name, 'details': [], 'id': self.id}
            for match in matches:
                for offset, name, bytes_ in match.strings:
                    result['details'].append({
                        'offset': offset,
                        'name': name,
                        'bytes': {'b64': str(base64.b64encode(bytes_))},
                    })
            return result
        return None


Indicator.datatypes[Yara.type] = Yara
