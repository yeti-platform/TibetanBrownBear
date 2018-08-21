"""Detail Yeti's Entity object structure."""
import json

from stix2 import parse_observable
from stix2 import exceptions

from yeti.core.errors import ValidationError
from .base import StixObject

class StixCYBOX(StixObject):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        if not self.validate_string(kwargs['value']):
            raise ValidationError(
                '{0:s} is not a valid string for {1:s}'.format(
                    kwargs['value'], self.type
                ))
        super().__init__(**kwargs)
        self.normalize()

    def _stix_parse(self, stix_dict):
        """Parses a dictionary into an actual STIX2 object.

        Args:
          stix_dict: The STIX dictionary to use to create the STIX obejct.

        Raises:
          ValidationError: If the dictionary does not comply with the STIX2
              standard.
        """
        if 'type' not in stix_dict:
            stix_dict['type'] = self.type
        try:
            self._stix_object = parse_observable(stix_dict)
        except (exceptions.MissingPropertiesError,
                exceptions.ParseError,
                exceptions.ExtraPropertiesError) as err:
            raise ValidationError(str(err))

    def update(self, args):
        """Updates a STIX Observable.

        Args:
          args: a {key:value} dicionary containing attributes to update.

        Returns:
          The new version of the STIX object.
        """
        args['type'] = self.type
        self._stix_parse(args)
        return self.save()

    def dump(self, destination='db'):
        """Dumps an Observable object into it's STIX JSON representation.

        Args:
          destination: Since STIX2 uses IDs as means to identify a single object
              we need to transform the object depending on whether it is being
              sent to the database or to a web client.

        Returns:
          The Observable's JSON representation in dictionary form.
        """
        serialized = json.loads(self._stix_object.serialize())
        if destination in ['db', 'web']:
            serialized['id'] = getattr(self, 'id', None)
        return serialized

    @classmethod
    def load(cls, args, strict=True):  # pylint: disable=unused-argument
        """Translate serialized information into a valid STIX definition.

        Will instantiate a STIX object from that definition.

        Args:
          args: The dictionary to use to create the STIX object.
          strict: Unused, kept to be consistent with overriden method

        Returns:
          The corresponding STIX objet.

        Raises:
          ValidationError: If a STIX object could not be instantiated from the
              serialized data.
        """
        return cls._load_stix(args)


    @property
    def type(self):
        return self._stix_object.type

    @property
    def value(self):
        return self._stix_object.value
