from marshmallow import fields, post_load
from yeti.core.model.database import YetiObject, YetiSchema

class SettingSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Setting objects."""
    name = fields.String(required=True)
    description = fields.String()
    settings = fields.Dict()
    type = fields.String()

    @post_load
    def load_setting(self, data):
        """Load a Setting object from its JSON representation.

        Returns:
          The created Setting object.
        """
        return Setting.datatypes[data['type']](**data)

class Setting(YetiObject):

    _collection_name = 'settings'
    _type_filter = None
    schema = SettingSchema

    name = None
    id = None
    settings = {}
    description = ''

    _indexes = [
        {'fields': ['name'], 'unique': True},
    ]
