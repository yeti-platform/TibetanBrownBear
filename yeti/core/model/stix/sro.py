"""Detail Yeti's Entity object structure."""
import json

from stix2.exceptions import MissingPropertiesError, ParseError
from stix2 import parse

from yeti.core.errors import ValidationError
from .base import StixObject

class StixSRO(StixObject):

    def __init__(self, db_from, db_to, attributes):
        self._db_from = db_from
        self._db_to = db_to
        super().__init__(**attributes)

    @classmethod
    def get(cls, key):
        """Fetches the most recent version of a STIX Relationship given its
            STIX ID.

        Args:
          key: The STIX ID of the Relationship to fetch.

        Returns:
          A STIX Relationship object.
        """
        all_versions = cls.filter({'attributes.id': key})
        if not all_versions:
            return None
        winner = all_versions[0]
        for version in all_versions:
            if version.modified > winner.modified:
                winner = version
        return winner

    def all_versions(self):
        """Returns all versions of a STIX object given its key.

        Returns:
          A list of STIX objects.
        """
        return super().filter({'attributes.id': self.id})

    def dump(self, destination='db'):
        """Dumps an Entity object into its STIX JSON representation.

        Args:
          destination: Since STIX2 uses IDs as means to identify a single object
              we need to transform the object depending on whether it is being
              sent to the database or to a web client.

        Returns:
          The Entity's JSON representation in dictionary form.
        """
        attributes = json.loads(self._stix_object.serialize())
        if destination == 'db':
            return {
                'id': self._arango_id,
                '_from': self._db_from,
                '_to': self._db_to,
                'attributes': attributes
            }
        return attributes


    @classmethod
    def _load_yeti(cls, args):
        """Translate information from the backend into a valid STIX definition.

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
        if isinstance(args, list):
            return [cls._load_yeti(item) for item in args]
        subclass = cls.get_final_datatype(args['attributes'])
        arango_id = args.pop('_id')
        db_from = args.pop('_from')
        db_to = args.pop('_to')
        args.pop('_rev', None)
        stix_rel = args['attributes']
        try:
            obj = subclass(db_from, db_to, stix_rel)
            obj._arango_id = arango_id
        except Exception as err:
            raise ValidationError(str(err))
        return obj

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