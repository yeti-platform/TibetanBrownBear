"""Detail Yeti's Observed Data object structure."""

from .entity import Entity

class ObservedData(Entity):
    """Observed Data Yeti object.

    Extends the ObservedData STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'observed-data'

    @property
    def first_observed(self):
        return self._stix_object.first_observed

    @property
    def last_observed(self):
        return self._stix_object.last_observed

    @property
    def number_observed(self):
        return self._stix_object.number_observed

    @property
    def objects(self):
        return self._stix_object.objects


Entity.datatypes[ObservedData.type] = ObservedData
