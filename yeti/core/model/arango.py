"""Class implementing a YetiConnector interface for ArangoDB."""

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
    """Yeti connector for an ArangoDB backend."""
    _db = DB

    def dump(self):
        """Dumps a Yeti object into a JSON representation.

        Returns:
          A JSON representation of the Yeti object."""
        return self._schema().dump(self).data

    def save(self):
        """Inserts a Yeti object into the database.

        Returns:
          The created Yeti object."""
        document_json = self.dump()
        if not self.key:
            del document_json['_key']
            result = self._get_collection().insert(
                document_json, return_new=True)
        else:
            result = self._get_collection().update(
                document_json, return_new=True)
        arangodoc = result['new']
        return self._schema().load(arangodoc).data

    @classmethod
    def list(cls):
        """Lists all objects.

        Returns:
          An arango.cursor.Cursor object"""
        return cls._schema(many=True).load(cls._get_collection().all()).data

    @classmethod
    def get(cls, key):
        """Fetches a single object by key.

        Args:
          key: ArangoDB _key value

        Returns:
          A Yeti object."""
        document = cls._get_collection().get(key)
        if document:
            return cls._schema().load(document).data
        return None

    @classmethod
    def filter(cls, args):
        colname = cls._collection_name
        observables = cls._db.aql.execute(
            'FOR o IN {0:s} FILTER o.value =~ @value RETURN o'.format(colname),
            bind_vars={'value': args['value']}
        )
        return cls._schema(many=True).load(observables).data


    @classmethod
    def _get_collection(cls):
        """Get the collection corresponding to this Yeti object class.

        Returns:
          The ArangoDB collection corresponding to the object class."""
        return COLLECTIONS[cls._collection_name]

    @classmethod
    def clear_db(cls):
        """Clears the ArangoDB database."""
        for collection in COLLECTIONS.values():
            collection.truncate()
