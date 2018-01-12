"""Interface definition for Yeti DB connectors."""

from marshmallow import Schema, fields

from .arango import ArangoYetiConnector

class YetiObject(ArangoYetiConnector):
    """Generic Yeti object.

    Attributes:
      _schema: a marshmallow.Schema class used for (de)serializing Yeti
          objects.
    """

    _schema = None

    @classmethod
    def collection_name(cls):
        """Return the collection or table name corresponding to this class.

        Returns;
          A string representing the collection name.
        """
        return cls._collection_name or cls.__name__.lower()


class YetiSchema(Schema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects.

    Attributes:
      key: Database primary key placeholder (marshmallow.fields.Int)
    """

    key = fields.Int(load_from='_key', dump_to='_key')
