from marshmallow import fields, post_load, validate
from yeti.core.model.database import YetiObject, YetiSchema

class UserSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for User objects."""
    email = fields.String(required=True, validate=validate.Email(error='Not a valid email'))
    password = fields.Str(allow_none=True)
    admin = fields.Boolean(missing=False)

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

    _indexes = [
        {'fields': ['email'], 'unique': True},
    ]

    def __repr__(self):
        return f'<User:{self.email}>'
