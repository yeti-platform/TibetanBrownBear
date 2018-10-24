"""Detail Yeti's Entity object structure."""
import json

from stix2 import parse
from stix2.exceptions import MissingPropertiesError, ParseError, UnmodifiablePropertyError
from stix2 import utils, Malware

from yeti.core.errors import ValidationError, YetiSTIXError
from .base import StixObject


class StixSDO(StixObject):

    # ===================================
    # These properties are common to all SDOs
    # Reference: http://docs.oasis-open.org/cti/stix/v2.0/cs01/part2-stix-objects/stix-v2.0-cs01-part2-stix-objects.html#_Toc496714302 # pylint: disable=line-too-long
    # ===================================

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
        try:
            self._stix_object = parse(stix_dict, allow_custom=True)
        except (MissingPropertiesError, ParseError) as err:
            raise ValidationError(str(err))

    def equals(self, stix_dict):
        for attribute, value in stix_dict.items():
            if getattr(self._stix_object, attribute, None) != value:
                return False
        return True

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
        for prop in utils.STIX_UNMOD_PROPERTIES:
            args.pop(prop, None)
        try:
            new_version = self._stix_object.new_version(**args, allow_custom=True)
        except (UnmodifiablePropertyError, MissingPropertiesError) as e:
            raise YetiSTIXError(str(e))
        self._stix_object = new_version
        return self.save()


    @classmethod
    def get(cls, key):
        """Fetches the most recent version of a STIX object given its
            STIX ID.

        Args:
          key: The STIX ID of the object to fetch.

        Returns:
          A STIX object.
        """
        all_versions = cls.filter({'stix_id': key})
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
        return super().filter({'stix_id': self.id})

    @classmethod
    def filter(cls, args):
        """Return the latest versions of matching STIX SDOs.

        Args:
            args: A key:value dictionary containing a 'value' or 'name' key
              defining the regular expression to match against.

        Returns:
          A List of Yeti objects.
        """
        all_versions = super().filter(args)
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
    def list(cls):
        """Lists all STIX 2 objects.

        By default, the latest version of all STIX SDOs is returned.

        Returns:
          An arango.cursor.Cursor object.
        """
        return cls._filter_latest_versions(super().list())

    def dump(self, destination='db'):
        """Dumps a STIX SDO object into its STIX JSON representation.

        Args:
          destination: Since STIX2 uses IDs as means to identify a single object
              we need to transform the object depending on whether it is being
              sent to the database or to a web client.

        Returns:
          The STIX SDO's JSON representation in dictionary form.
        """
        serialized = json.loads(self._stix_object.serialize())
        if destination == 'db':
            serialized['stix_id'] = serialized['id']
            serialized['id'] = None
        return serialized

    @classmethod
    def load(cls, args, strict=True):  # pylint: disable=unused-argument
        """Load a serialized STIX object from the database."""
        return cls._load_stix(args)

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
