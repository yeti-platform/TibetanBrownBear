"""Detail Yeti's Report object structure."""

from .entity import Entity

class Report(Entity):
    """Report Yeti object.

    Extends the Report STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'report'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def published(self):
        return self._stix_object.published

    @property
    def object_refs(self):
        return self._stix_object.object_refs


Entity.datatypes[Report.type] = Report
