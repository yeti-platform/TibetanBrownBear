"""Detail Yeti's incident object structure."""
from stix2 import CustomObject, properties

from .entity import Entity


@CustomObject('x-incident', [
    ('x_internal_references', properties.ListProperty(properties.StringProperty)),
    ('name', properties.StringProperty()),
    ('description', properties.StringProperty()),
])
class StixIncident():
    _collection_name = 'entities'
    type = 'x-incident'

    @property
    def internal_references(self):
        return self._stix_object.internal_references

class Incident(Entity):
    """Incident Yeti object."""

    _collection_name = 'entities'
    type = 'x-incident'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

Entity.datatypes[Incident.type] = Incident
