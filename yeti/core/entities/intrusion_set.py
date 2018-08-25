"""Detail Yeti's Threat Instrusion Set object structure."""

from .entity import Entity

class IntrusionSet(Entity):
    """Threat Instrusion Set Yeti object.

    Extends the IntrusionSet STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'intrusion-set'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def aliases(self):
        return self._stix_object.aliases

    @property
    def first_seen(self):
        return self._stix_object.first_seen

    @property
    def last_seen(self):
        return self._stix_object.last_seen

    @property
    def goals(self):
        return self._stix_object.goals

    @property
    def resource_level(self):
        return self._stix_object.resource_level

    @property
    def primary_motivation(self):
        return self._stix_object.primary_motivation

    @property
    def secondary_motivations(self):
        return self._stix_object.secondary_motivations

Entity.datatypes[IntrusionSet.type] = IntrusionSet
