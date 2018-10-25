"""Detail Yeti's Entity object structure."""

from yeti.core.model.stix import StixSRO

class BaseRelationship(StixSRO):

    _collection_name = 'relationships'
    type = None
    _type_filter = None

