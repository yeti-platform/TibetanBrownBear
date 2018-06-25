"""Detail Yeti's Entity object structure."""
import json

from stix2 import parse_observable
from stix2.exceptions import MissingPropertiesError, ParseError

from yeti.core.errors import ValidationError, IntegrityError
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
        except (MissingPropertiesError, ParseError) as err:
            raise ValidationError(str(err))

    def update(self, args):
        """Updates a STIX Observable.

        Args:
          args: a {key:value} dicionary containing attributes to update.

        Returns:
          The new version of the STIX object.
        """
        args['type'] = self.type
        self._stix_object = self._stix_parse(args)
        return self.save()

    @classmethod
    def get(cls, value):
        """Fetches a STIX observable from the database given its value.

        Returns:
          A STIX object.
        """
        return cls.find(value=value)

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
        if destination == 'db':
            serialized['id'] = getattr(self, 'id', None)
        return serialized

    @classmethod
    def load(cls, args, strict=True):
        """Translate information from the backend into a valid STIX definition.

        Will instantiate a STIX object from that definition.

        Args:
          args: The dictionary to use to create the STIX object.
          strict: Unused, kept to be consistent with overriden method

        Returns:
          The corresponding STIX objet.

        Raises:
          IntegrityError: If a STIX object could not be instantiated from the
              data in the database.
        """
        subclass = cls.get_final_datatype(args)
        if isinstance(args, list):
            return [subclass.load(item) for item in args]
        args['id'] = args.pop('_key', None)
        args.pop('_id', None)
        args.pop('_rev', None)
        try:
            observable = subclass(**args)
            return observable
        except Exception as err:
            raise IntegrityError(str(err))


    @property
    def type(self):
        return self._stix_object.type

    @property
    def value(self):
        return self._stix_object.value
