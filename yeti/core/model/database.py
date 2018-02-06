"""Interface definition for Yeti DB connectors."""


from .arango import ArangoYetiConnector, ArangoYetiSchema


class YetiObject(ArangoYetiConnector):
    """Generic Yeti object.

    Attributes:
      _schema: a marshmallow.Schema class used for (de)serializing Yeti
          objects.
    """

    _schema = None
    _indexes = []

class YetiSchema(ArangoYetiSchema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects."""
    pass
