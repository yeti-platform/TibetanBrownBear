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

    @classmethod
    def collection_name(cls):
        """Return the collection or table name corresponding to this class.

        Returns;
          A string representing the collection name.
        """
        return cls._collection_name or cls.__name__.lower()


class YetiSchema(ArangoYetiSchema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects."""
    pass
