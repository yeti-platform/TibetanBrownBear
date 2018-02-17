"""Interface definition for Yeti DB connectors."""


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

    @classmethod
    def load_object_from_type(cls, obj, strict=False):
        objtype = cls.datatypes.get(obj.get('type'), cls)
        return objtype.schema(strict=strict).load(obj).data

    @classmethod
    def get_realschema(cls, obj):
        return cls.datatypes.get(obj.get('type'), cls).schema


class YetiSchema(ArangoYetiSchema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects."""
    pass
