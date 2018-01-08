from arango import ArangoClient

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='',
    enable_logging=True
)

DB = client.database('yeti')

 # exhaustive list of needed collections here
collections = [
    'observable',
]

COLLECTIONS = dict()
for collection_name in collections:
    COLLECTIONS[collection_name] = DB.collection(collection_name)

class ArangoYetiConnector:

    _db = DB

    def dump(self):
        return self._schema.dump(self).data

    def save(self):
        document_json = self.dump()
        if not self.key:
            del document_json['_key']
            result = self._get_collection().insert(
                document_json, return_new=True)
        else:
            result = self._get_collection().update(
                document_json, return_new=True)
        arangodoc = result['new']
        return self._schema.load(arangodoc).data

    @classmethod
    def list(cls):
        # TODO implement loading from marshmallow schema with many=True
        return cls._get_collection().all()

    @classmethod
    def get(cls, key):
        document = cls._get_collection().get(key)
        return cls._schema.load(document).data

    @classmethod
    def _get_collection(cls):
        return COLLECTIONS[cls._collection_name]

    @classmethod
    def clear_db(cls):
        for collection in COLLECTIONS.values():
            collection.truncate()
