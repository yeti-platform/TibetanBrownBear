"""Detail the Yeti's Observable object structure."""

from marshmallow import fields, post_load

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
        print( "Constructing", self.constructor, "from", data)
        return self.constructor(**data)


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

    def __repr__(self):
        return '<{type!r}(value={value!r})>'.format(
            type=self.__class__.__name__,
            value=self.value)

    @classmethod
    def is_valid(cls, text):
        if text is not None:
            return True
        return False

ObservableSchema.constructor = Observable
