"""Detail Yeti's Threat Campaign object structure."""

from .entity import Entity

class Campaign(Entity):
    """Threat Campaign Yeti object.

    Extends the Campaign STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'campaign'

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
    def objective(self):
        return self._stix_object.objective


Entity.datatypes[Campaign.type] = Campaign
