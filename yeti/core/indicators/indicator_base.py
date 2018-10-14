"""Detail Yeti's Indicator object structure."""

from yeti.core.model.stix import StixSDO

class Indicator(StixSDO):

    _collection_name = 'entities' # make graphs easier
    type = 'indicator'
    _type_filter = None
    _indexes = [
        {'fields': ['name'], 'unique': False},
    ]
    _text_indexes = [
        {'fields': ['name']},
    ]
