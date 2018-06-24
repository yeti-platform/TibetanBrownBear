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

    @classmethod
    def get_final_datatype(cls, args):
        subclass = cls
        if 'type' in args:
            if args['type'] not in cls.datatypes:
                raise ValidationError(
                    '"{0:s}" not in acceptable datatypes ({1!r})'.format(
                        args['type'], cls.datatypes))
            subclass = cls.datatypes[args['type']]
        return subclass
