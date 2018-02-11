"""Detail the Yeti's Entity object structure."""

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

        @post_load means this will be called after eath marshmallow.load call.

        Returns:
          The Entity object.
        """
        datatype = DATATYPES[data['type']]
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
    _schema = EntitySchema

    id = None
    name = None
    type = 'entity'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.is_valid()

    def __repr__(self):
        return '<{type:s}(name={name!r})>'.format(
            type=self.__class__.__name__,
            name=self.name)

    def is_valid(self):
        if not isinstance(self.name, str):
            raise ValidationError(".name must be a string.")
        return True

DATATYPES = {
    'entity': Entity,
}
