"""Detail Yeti's Entity object structure."""
import json

from dateutil import parser
from marshmallow import fields, post_load
from stix2 import parse
from stix2.exceptions import MissingPropertiesError, ParseError

from yeti.core.errors import ValidationError
from ..model.database import YetiObject, YetiSchema

class Entity(YetiObject):
    """Entity Yeti object.

    Attributes:
      key: Database primary key
      name: Entity name
    """

    _collection_name = 'entities'
    _indexes = [
        {'fields': ['name'], 'unique': False},
    ]
    _text_indexes = [
        {'fields': ['name']},
    ]

    def _stix_parse(self, stix_dict):
        stix_dict['type'] = self.stix_type
        try:
            self._stix_object = parse(stix_dict)
        except (MissingPropertiesError, ParseError) as err:
            raise ValidationError(err)

    def __init__(self, **stix_dict):
        self._stix_parse(stix_dict)

    @classmethod
    def load(cls, stix_dict, strict=False):
        stix_dict.pop('_key')
        stix_dict.pop('_id')
        stix_dict.pop('_rev')
        stix_dict['id'] = stix_dict.pop('stix_id')
        try:
            return cls(**stix_dict)
        except Exception as err:
            raise ValidationError(err)

    def dump(self):
        serialized = json.loads(self._stix_object.serialize())
        serialized['stix_id'] = serialized['id']
        serialized['id'] = None
        return serialized

    def all_versions(self):
        return self.filter({'stix_id': self._stix_object.id})

    @classmethod
    def get(cls, key):
        all_versions = cls.filter({'stix_id': key})
        modified = all_versions[0]._stix_object.modified
        winner = all_versions[0]
        for version in all_versions:
            parsed_timestamp = version._stix_object.modified
            if parsed_timestamp > modified:
                modified = parsed_timestamp
                winner = version
        return winner

    def update(self, args):
        new_version = self._stix_object.new_version(**args)
        self._stix_object = new_version
        return self.save()

    # def save(self):
    #     return YetiObject.save(self)


    def __repr__(self):
        return str(self._stix_object)
