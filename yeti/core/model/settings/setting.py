from marshmallow import fields, post_load
from yeti.core.model.database import YetiObject, YetiSchema

class SettingSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Setting objects."""
    name = fields.String(required=True)
    settings = fields.Dict()

    @post_load
    def load_tag(self, data):
        """Load a Tag object from its JSON representation.

        Returns:
          The created Tag object.
        """
        name = data['name']
        return Setting.types[name](**data)

class Setting(YetiObject):

    _collection_name = 'settings'
    schema = SettingSchema

    name = None
    id = None
    settings = {}
    types = {}
