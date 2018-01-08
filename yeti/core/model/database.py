
from marshmallow import Schema, fields

from .arango import ArangoYetiConnector

class YetiObject(ArangoYetiConnector):

    _schema = None

    @classmethod
    def collection_name(klass):
        return klass._collection_name or klass.__name__.lower()


class YetiSchema(Schema):
    key = fields.Int(load_from='_key', dump_to='_key')
