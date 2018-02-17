"""Interface definition for Yeti DB connectors."""


from yeti.core.errors import ValidationError
from .arango import ArangoYetiConnector, ArangoYetiSchema

class YetiObject(ArangoYetiConnector):
    """Generic Yeti object.

    Attributes:
      schema: a marshmallow.Schema class used for (de)serializing Yeti
          objects.
    """

    schema = None
    _indexes = []
    datatypes = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.is_valid()

    def __repr__(self):
        return '<{type:s}({key!r})>'.format(
            type=self.__class__.__name__,
            key=self.value if hasattr(self, 'value') else self.name)

    @classmethod
    def load_object_from_type(cls, obj, strict=False):
        objtype = cls.datatypes.get(obj.get('type'), cls)
        return objtype.schema(strict=strict).load(obj).data

    @classmethod
    def get_realschema(cls, obj):
        return cls.datatypes.get(obj.get('type'), cls).schema

    def is_valid(self):
        return True


class YetiSchema(ArangoYetiSchema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects."""

    def handle_error(self, exc, data):  #pylint: disable=arguments-differ
        """Log and raise our custom exception when (de)serialization fails."""
        raise ValidationError(exc.messages)
