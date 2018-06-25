"""Detail Yeti's Entity object structure."""
from abc import abstractmethod

from yeti.core.model.database import YetiObject

class StixObject(YetiObject):
    """Entity Yeti object.

    Attributes:
      key: Database primary key
      name: Entity name
    """

    @abstractmethod
    def _stix_parse(self, stix_dict):
        """Parses a dictionary into an actual STIX2 SDO or Observable.

        Args:
          stix_dict: The dictionary to use to create the STIX obejct.

        Raises:
          ValidationError: If the dictionary does not comply with the STIX2
              standard.
        """
        raise NotImplementedError

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

    @classmethod
    def list(cls):
        """Lists all STIX 2 objects.

        By default, the latest version of all STIX SDOs is returned.

        Returns:
          An arango.cursor.Cursor object.
        """
        return super().list()

    def __repr__(self):
        return str(self._stix_object)
