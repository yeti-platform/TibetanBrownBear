"""Detail the Yeti's Observable object structure."""

from marshmallow import fields, post_load

from ..model.database import YetiObject, YetiSchema

class ObservableSchema(YetiSchema):
    value = fields.String(required=True)

    @post_load
    def load_observable(self, data):
        return Observable(**data)

class Observable(YetiObject):

    _collection_name = 'observable'
    _schema = ObservableSchema()

    key = None
    value = None

    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.value = kwargs['value']

    # def __repr__(self):
    #     return '<Observable(value={value!r})>'.format(value=self.value)
