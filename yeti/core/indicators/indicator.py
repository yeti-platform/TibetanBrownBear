"""Detail the Yeti's Indicator object structure."""

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from ..model.database import YetiObject, YetiSchema

class IndicatorSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Indicator objects."""
    name = fields.String(required=True)
    type = fields.String()

    @post_load
    def load_indicator(self, data):
        """Load an Indicator object from its JSON representation.

        @post_load means this will be called after eath marshmallow.load call.

        Returns:
          The Indicator object.
        """
        datatype = Indicator.datatypes.get(data['type'], Indicator)
        object_ = datatype(**data)
        return object_

class Indicator(YetiObject):
    """Indicator Yeti object.

    Attributes:
      key: Database primary key
      name: Indicator name
    """

    _collection_name = 'indicators'
    _indexes = [
        {'fields': ['name'], 'unique': True},
    ]
    _schema = IndicatorSchema
    datatypes = {}

    id = None
    name = None
    type = 'indicator'

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
