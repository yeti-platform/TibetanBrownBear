"""Detail Yeti's AttackPattern object structure."""

from .entity import Entity

class AttackPattern(Entity):
    """AttackPattern Yeti object.

    Extends the AttackPattern STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'attack-pattern'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def kill_chain_phases(self):
        return self._stix_object.kill_chain_phases

Entity.datatypes[AttackPattern.type] = AttackPattern
