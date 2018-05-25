"""Detail Yeti's Indicator object structure."""

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

        @post_load means this will be called after each marshmallow.load call.

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
    schema = IndicatorSchema

    id = None
    name = None
    type = 'indicator'

    def is_valid(self):
        if not isinstance(self.name, str):
            raise ValidationError('.name must be a string.')
        return True

    def match(self, obj):
        """Matches this indicators against an object.

        Args:
          obj: An object to match the Indicator on

        Returns:
          A list of dicts representing matches.
        """
        raise NotImplementedError
