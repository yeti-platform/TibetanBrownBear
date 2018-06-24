"""Detail Yeti's Entity object structure."""

from yeti.core.stix_sdo import StixSDO

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

    @classmethod
    def get_final_datatype(cls, args):
        subclass = cls
        if 'type' in args:
            subclass = cls.datatypes[args['type']]
        return subclass
