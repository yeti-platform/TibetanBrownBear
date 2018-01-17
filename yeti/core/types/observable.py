"""Detail the Yeti's Observable object structure."""

from marshmallow import fields, post_load

from ..model.database import YetiObject, YetiSchema


class ObservableSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Observable objects."""
    value = fields.String(required=True)

    @post_load
    def load_observable(self, data):
        """Load an Observable object from its JSON representation.

        @post_load means this will be called after eath marshmallow.load call.

        Returns:
          The Observable object.
        """
        return Observable(**data)


class Observable(YetiObject):
    """Observable Yeti object.

    Attribuets:
      key: Database primary key
      value: Observable value
    """

    _collection_name = 'observable'
    _schema = ObservableSchema

    id = None
    value = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.value = kwargs['value']

    # def __repr__(self):
    #     return '<Observable(value={value!r})>'.format(value=self.value)
