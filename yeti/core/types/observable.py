"""Detail the Yeti's Observable object structure."""

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from ..model.database import YetiObject, YetiSchema

class ObservableSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Observable objects."""
    value = fields.String(required=True)
    type = fields.Constant("observable")

    @post_load
    def load_observable(self, data):
        """Load an Observable object from its JSON representation.

        @post_load means this will be called after eath marshmallow.load call.

        Returns:
          The Observable object.
        """
        object_ = self.constructor(**data)
        object_.normalize()
        return object_


class Observable(YetiObject):
    """Observable Yeti object.

    Attributes:
      key: Database primary key
      value: Observable value
    """

    _collection_name = 'observables'
    _schema = ObservableSchema

    id = None
    value = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.is_valid()

    def __repr__(self):
        return '<{type!r}(value={value!r})>'.format(
            type=self.__class__.__name__,
            value=self.value)

    def is_valid(self):
        if self.value is not None:
            return True
        raise ValidationError

    def normalize(self):
        pass

ObservableSchema.constructor = Observable
