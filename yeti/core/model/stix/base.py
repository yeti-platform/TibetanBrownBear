"""Detail Yeti's Entity object structure."""
import json

from stix2 import parse
from stix2 import versioning
from stix2.exceptions import MissingPropertiesError, ParseError, UnmodifiablePropertyError

from yeti.core.errors import ValidationError, YetiSTIXError
from yeti.core.model.database import YetiObject


class StixObject(YetiObject):
    """Entity Yeti object.

    Attributes:
      key: Database primary key
      name: Entity name
    """

    def __init__(self, **stix_dict):
        """Initializes an Entity's STIX object.

        Args:
          stix_dict: The dictionary to use to create the STIX object.
        """
        self._stix_object = None
        self._stix_parse(stix_dict)
        super().__init__()

    @classmethod
    def from_stix_object(cls, stix_object):
        """Creates a YetiObject instance from a native STIX object."""
        return cls(**json.loads(stix_object.serialize()))

    @classmethod
    def list(cls):
        """Lists all STIX 2 objects.

        By default, the latest version of all STIX SDOs is returned.

        Returns:
          An arango.cursor.Cursor object.
        """
        return cls._filter_latest_versions(super().list())

    @classmethod
    def filter(cls, args, latest=True, offset=None, count=None):
        """Return matching STIX SDOs.

        Args:
            args: A key:value dictionary containing a 'value' or 'name' key
                defining the regular expression to match against.
            latest: If True, only return the latest revision of the objects in
                the filter.

        Returns:
          A List of Yeti objects.
        """
        all_versions = super().filter(args, offset, count)
        if not latest:
            return all_versions
        return cls._filter_latest_versions(all_versions)

    @classmethod
    def _filter_latest_versions(cls, all_versions):
        """Filters a list of Yeti objects, keeping the most recent version of
        each."""
        latest_versions = {}
        for version in all_versions:
            stored = latest_versions.get(version.id)
            if not stored:
                latest_versions[version.id] = version
                continue
            if version.modified > stored.modified:
                latest_versions[version.id] = version
        return list(latest_versions.values())

    @classmethod
    def load(cls, args, strict=True):  # pylint: disable=unused-argument
        """Load a serialized STIX object from the database."""
        return cls.load_stix(args)

    def _stix_parse(self, stix_dict):
        """Parses a dictionary into an actual STIX2 SDO.

        Args:
          stix_dict: The dictionary to use to create the STIX obejct.

        Raises:
          ValidationError: If the dictionary does not comply with the STIX2
              standard.
        """
        if 'type' not in stix_dict:
            stix_dict['type'] = self.type
        if 'spec_version' not in stix_dict:
            # spec version needs to be specified for STIX to find our custom
            # objects.
            stix_dict['spec_version'] = '2.1'
        try:
            self._stix_object = parse(stix_dict, allow_custom=True)
        except (MissingPropertiesError, ParseError) as err:
            raise ValidationError(str(err))

    def update(self, args):
        """Updates a STIX object, creating a new version.

        Args:
          args: a {key:value} dicionary containing attributes to update.

        Returns:
          The new version of the STIX object.
        """
        if self.equals(args):
            return self
        for key, value in args.items():
            if not value:
                args[key] = None
        for prop in versioning.STIX_UNMOD_PROPERTIES:
            args.pop(prop, None)
        try:
            new_version = self._stix_object.new_version(**args, allow_custom=True)
        except (UnmodifiablePropertyError, MissingPropertiesError) as e:
            raise YetiSTIXError(str(e))
        self._stix_object = new_version
        return self.save()

    def get_extended_property(self, property_name):
        return getattr(self._stix_object, property_name)

    def equals(self, stix_dict):
        for attribute, value in stix_dict.items():
            if getattr(self._stix_object, attribute, None) != value:
                return False
        return True

    def __repr__(self):
        return str(self._stix_object)
