"""Detail Yeti's Identity object structure."""

from .entity import Entity

class Identity(Entity):
    """Identity Yeti object.

    Extends the Identity STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'identity'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def identity_class(self):
        return self._stix_object.identity_class

    @property
    def sectors(self):
        return self._stix_object.sectors

    @property
    def contact_information(self):
        return self._stix_object.contact_information

Entity.datatypes[Identity.type] = Identity
