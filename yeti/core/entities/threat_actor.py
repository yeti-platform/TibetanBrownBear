"""Detail Yeti's Threat Actor object structure."""

from .entity import Entity

class ThreatActor(Entity):
    """Threat Actor Yeti object.

    Extends the ThreatActor STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'threat-actor'

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
    def roles(self):
        return self._stix_object.roles

    @property
    def goals(self):
        return self._stix_object.goals

    @property
    def sophistication(self):
        return self._stix_object.sophistication

    @property
    def resource_level(self):
        return self._stix_object.resource_level

    @property
    def primary_motivation(self):
        return self._stix_object.primary_motivation

    @property
    def secondary_motivations(self):
        return self._stix_object.secondary_motivations

    @property
    def personal_motivations(self):
        return self._stix_object.personal_motivations

Entity.datatypes[ThreatActor.type] = ThreatActor
