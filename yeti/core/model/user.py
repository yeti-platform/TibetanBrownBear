from marshmallow import fields, post_load, validate
from yeti.core.model.database import YetiObject, YetiSchema
from yeti.core.model.fields import RealDateTime

class UserSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for User objects."""
    email = fields.String(required=True, validate=validate.Email(error='Not a valid email'))
    password = fields.Str(allow_none=True)
    admin = fields.Boolean(missing=False)
    api_key = fields.Str(allow_none=True)
    last_password_change = RealDateTime()

    @post_load
    def load_user(self, data):
        """Load a User object from its JSON representation.

        Returns:
          The created Tag object.
        """
        return User(**data)

class User(YetiObject):

    _collection_name = 'users'
    schema = UserSchema

    id = None
    email = None
    password = None
    admin = False
    api_key = None
    last_password_change = None

    _indexes = [
        {'fields': ['email'], 'unique': True},
    ]

    def dump(self, destination='db'):
        serialized = super().dump()
        if destination == 'web':
            serialized.pop('password')
        return serialized

    def __repr__(self):
        return f'<User:{self.email}>'
