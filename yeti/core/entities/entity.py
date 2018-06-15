"""Detail Yeti's Entity object structure."""

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from ..model.database import YetiObject, YetiSchema

class EntitySchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Entity objects."""
    name = fields.String(required=True)
    type = fields.String()

    @post_load
    def load_entity(self, data):
        """Load an Entity object from its JSON representation.

        @post_load means this will be called after each marshmallow.load call.

        Returns:
          The Entity object.
        """
        datatype = Entity.datatypes.get(data['type'], Entity)
        object_ = datatype(**data)
        return object_

class Entity(YetiObject):
    """Entity Yeti object.

    Attributes:
      key: Database primary key
      name: Entity name
    """

    _collection_name = 'entities'
    _indexes = [
        {'fields': ['name'], 'unique': True},
    ]
    _text_indexes = [
        {'fields': ['name']},
    ]
    schema = EntitySchema

    id = None
    name = None
    type = 'entity'

    def is_valid(self):
        if not self.name or not isinstance(self.name, str):
            msg = 'Invalid \'name\' parameter (provided {0:s})'.format(
                repr(self.name))
            raise ValidationError(msg)
        return True
