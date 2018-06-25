"""Detail Yeti's Entity object structure."""

from yeti.core.model.stix import StixSDO
from yeti.core.errors import ValidationError

class Entity(StixSDO):

    _collection_name = 'entities'
    type = None
    _type_filter = None
    _indexes = [
        {'fields': ['name'], 'unique': False},
    ]
    _text_indexes = [
        {'fields': ['name']},
    ]
