"""Detail Yeti's Entity object structure."""
import json

from .base import StixObject


class StixSDO(StixObject):

    # ===================================
    # These properties are common to all SDOs
    # Reference: http://docs.oasis-open.org/cti/stix/v2.0/cs01/part2-stix-objects/stix-v2.0-cs01-part2-stix-objects.html#_Toc496714302 # pylint: disable=line-too-long
    # ===================================

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
        return super().filter({'stix_id': self.id}, latest=False)

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
