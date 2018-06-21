"""Detail Yeti's Entity object structure."""
import json

from stix2 import parse
from stix2.exceptions import MissingPropertiesError, ParseError

from yeti.core.errors import ValidationError, IntegrityError
from ..model.database import YetiObject

class Entity(YetiObject):
    """Entity Yeti object.

    Attributes:
      key: Database primary key
      name: Entity name
    """

    _collection_name = 'entities'
    _indexes = [
        {'fields': ['name'], 'unique': False},
    ]
    _text_indexes = [
        {'fields': ['name']},
    ]

    def _stix_parse(self, stix_dict):
        """Parses a dictionary into an actual STIX2 object.

        Args:
          stix_dict: The STIX dictionary to use to create the STIX obejct.

        Raises:
          ValidationError: If the dictionary does not comply with the STIX2
              standard.
        """
        stix_dict['type'] = self.stix_type
        try:
            self._stix_object = parse(stix_dict)
        except (MissingPropertiesError, ParseError) as err:
            raise ValidationError(err)

    # We don't want to call YetiObject's init method since this would set all
    # attributes in stix_dict in the Entity object; we want them in
    # _stix_object.
    # pylint: disable=super-init-not-called
    def __init__(self, **stix_dict):
        """Initializes an Entity's STIX object.

        Args:
          stix_dict: The dictionary to use to create the STIX object.
        """
        self._stix_object = None
        self._stix_parse(stix_dict)

    # We want to call this argument stix_dict instead of the generic "args" in
    # YetiObject.
    # pylint: disable=arguments-differ
    @classmethod
    def load(cls, stix_dict):
        """Translate information from the backend into a valid STIX definition.

        Will instantiate a STIX object from that definition.

        Args:
          stix_dict: The dictionary to use to create the STIX object.

        Returns:
          The corresponding STIX objet.

        Raises:
          IntegrityError: If a STIX object could not be instantiated from the
              data in the database.
        """
        stix_dict.pop('_key')
        stix_dict.pop('_id')
        stix_dict.pop('_rev')
        stix_dict['id'] = stix_dict.pop('stix_id')
        try:
            return cls(**stix_dict)
        except Exception as err:
            raise IntegrityError(err)

    def dump(self):
        """Dumps an Entity object into it's STIX JSON representation.

        Returns:
          The Entity's JSON representation in dictionary form.
        """
        serialized = json.loads(self._stix_object.serialize())
        serialized['stix_id'] = serialized['id']
        serialized['id'] = None
        return serialized

    def all_versions(self):
        """Returns all versions of a STIX object given its key.

        Returns:
          A list of STIX objects.
        """
        return self.filter({'stix_id': self.id})

    @classmethod
    def get(cls, key):
        """Fetches the most recent version of a STIX object given its key.

        Returns:
          A STIX object.
        """
        all_versions = cls.filter({'stix_id': key})
        modified = all_versions[0].modified
        winner = all_versions[0]
        for version in all_versions:
            parsed_timestamp = version.modified
            if parsed_timestamp > modified:
                modified = parsed_timestamp
                winner = version
        return winner

    def update(self, args):
        """Updates a STIX object, creating a new version.

        Args:
          args: a {key:value} dicionary containing attributes to update.

        Returns:
          The new version of the STIX object.
        """
        new_version = self._stix_object.new_version(**args)
        self._stix_object = new_version
        return self.save()

    def __repr__(self):
        return str(self._stix_object)

    @property
    def type(self):
        return self._stix_object.type

    @property
    def id(self):
        return self._stix_object.id

    @property
    def created_by_ref(self):
        return self._stix_object.created_by_ref

    @property
    def created(self):
        return self._stix_object.created

    @property
    def modified(self):
        return self._stix_object.modified

    @property
    def revoked(self):
        return self._stix_object.revoked

    @property
    def labels(self):
        return self._stix_object.labels

    @property
    def external_references(self):
        return self._stix_object.external_references

    @property
    def object_marking_refs(self):
        return self._stix_object.object_marking_refs

    @property
    def granular_markings(self):
        return self._stix_object.granular_markings
