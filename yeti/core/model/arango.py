"""Class implementing a YetiConnector interface for ArangoDB."""
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError

from yeti.common.config import yeti_config


class ArangoDatabase:
    """Class that contains the base class for the database.

    Essentially a proxy that will delay the connection to the first call.
    """

    def __init__(self):
        self.db = None
        self.collections = dict()

    def connect(self):
        client = ArangoClient(
            protocol='http',
            host=yeti_config.arangodb.host,
            port=yeti_config.arangodb.port,
            username=yeti_config.arangodb.username,
            password=yeti_config.arangodb.password,
            enable_logging=True)

        # Create database if it does not exist
        try:
            client.create_database(yeti_config.arangodb.database)
        except DatabaseCreateError as err:
            # 12707 - ERROR_ARANGO_DUPLICATE_NAME
            # https://docs.arangodb.com/3.0/Manual/Appendix/ErrorCodes.html
            if not err.error_code == 1207:
                raise

        self.db = client.database(yeti_config.arangodb.database)

    def clear(self):
        for name in self.collections:
            self.collections[name].truncate()

    def collection(self, name):
        if self.db is None:
            self.connect()

        if name not in self.collections:
            # Create collection if it does not exist
            try:
                self.db.create_collection(name)
            except CollectionCreateError as err:
                # 12707 - ERROR_ARANGO_DUPLICATE_NAME
                # https://docs.arangodb.com/3.0/Manual/Appendix/ErrorCodes.html
                if not err.error_code == 1207:
                    raise

            self.collections[name] = self.db.collection(name)

        return self.collections[name]

    def __getattr__(self, key):
        if self.db is None:
            self.connect()

        return getattr(self.db, key)


db = ArangoDatabase()


class ArangoYetiConnector:
    """Yeti connector for an ArangoDB backend."""
    _db = db

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
            bind_vars={
                'value': args['value']
            })
        return cls._schema(many=True).load(observables).data

    @classmethod
    def _get_collection(cls):
        """Get the collection corresponding to this Yeti object class.

        Returns:
          The ArangoDB collection corresponding to the object class."""
        return cls._db.collection(cls._collection_name)
