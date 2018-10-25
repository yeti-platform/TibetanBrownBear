from .base import BaseRelationship


class Relationship(BaseRelationship):
    """Relationship Yeti object.

    Extends the Relationship STIX2 definition.
    """

    type = 'relationship'

    @property
    def relationship_type(self):
        return self._stix_object.relationship_type

    @property
    def description(self):
        return self._stix_object.description

    @property
    def source_ref(self):
        return self._stix_object.source_ref

    @property
    def target_ref(self):
        return self._stix_object.target_ref

BaseRelationship.datatypes[Relationship.type] = Relationship
