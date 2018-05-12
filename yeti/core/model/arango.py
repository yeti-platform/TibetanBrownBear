"""Class implementing a YetiConnector interface for ArangoDB."""
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError, DocumentInsertError, GraphCreateError, EdgeDefinitionCreateError  # pylint: disable=line-too-long
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from yeti.core.errors import ValidationError, IntegrityError

from yeti.common.config import yeti_config
from .interfaces import AbstractYetiConnector

LINK_TYPE_TO_GRAPH = {
    'tagged': 'tags',
    'uses': 'entities',
}

class ArangoDatabase:
    """Class that contains the base class for the database.

    Essentially a proxy that will delay the connection to the first call.
    """

    def __init__(self):
        self.db = None
        self.collections = dict()
        self.graphs = dict()
        self.create_edge_definition(self.graph('tags'), {
            'edge_collection': 'tagged',
            'from_vertex_collections': ['observables'],
            'to_vertex_collections': ['tags'],
        })
        self.create_edge_definition(self.graph('entities'), {
            'edge_collection': 'uses',
            'from_vertex_collections': ['entities'],
            'to_vertex_collections': ['observables', 'entities'],
        })
        # entities, observables, and tags are already created
        self.collection('indicators')


    def connect(self):
        client = ArangoClient(
            protocol='http',
            host=yeti_config.arangodb.host,
            port=yeti_config.arangodb.port)

        sys_db = client.db('_system')
        if not sys_db.has_database(yeti_config.arangodb.database):
            sys_db.create_database(yeti_config.arangodb.database)

        self.db = client.db(yeti_config.arangodb.database,
                            username=yeti_config.arangodb.username,
                            password=yeti_config.arangodb.password)

    def clear(self):
        for name in self.collections:
            self.collections[name].truncate()

    def collection(self, name):
        if self.db is None:
            self.connect()

        if name not in self.collections:
            if self.db.has_collection(name):
                self.collections[name] = self.db.collection(name)
            else:
                self.collections[name] = self.db.create_collection(name)

        return self.collections[name]

    def graph(self, name):
        if self.db is None:
            self.connect()

        try:
            return self.db.create_graph(name)
        except GraphCreateError as err:
            if err.error_code in [1207, 1925]:
                return self.db.graph(name)
            raise

    def create_edge_definition(self, graph, definition):
        if self.db is None:
            self.connect()

        if graph.has_edge_definition(definition['edge_collection']):
            return graph.edge_collection(definition['edge_collection'])
        return graph.create_edge_definition(**definition)

    def __getattr__(self, key):
        if self.db is None:
            self.connect()

        return getattr(self.db, key)


db = ArangoDatabase()

class ArangoYetiSchema(Schema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects.

    Attributes:
      id: Database primary key placeholder (marshmallow.fields.Int)
    """

    id = fields.Int(load_from='_key', dump_to='_key')
    _arango_id = fields.Str(load_from='_id', dump_to='_id')

class ArangoYetiConnector(AbstractYetiConnector):
    """Yeti connector for an ArangoDB backend."""
    _db = db

    @classmethod
    def load(cls, args, strict=False):
        """Loads data from a dictionary into the corresponding YetiObject.

        Args:
          args: key:value dictionary with which to populate fields in the
              YetiObject
        """
        try:
            if isinstance(args, list):
                return [cls.load(doc, strict=strict) for doc in args]
            return cls.load_object_from_type(args, strict=strict)
        except MarshmallowValidationError as e:
            raise ValidationError(e.messages)

    def dump(self):
        """Dumps a Yeti object into a JSON representation.

        Returns:
          A JSON representation of the Yeti object.
        """
        data = self.schema().dump(self).data
        if '_key' in data:
            data['id'] = data.pop('_key')
        return data

    def save(self):
        """Inserts a Yeti object into the database.

        Returns:
          The created Yeti object."""
        document_json = self.schema().dump(self).data
        if not self.id:
            del document_json['_key']
            try:
                result = self._get_collection().insert(
                    document_json, return_new=True)
            except DocumentInsertError as err:
                if not err.error_code == 1210: # Unique constraint violation
                    raise
                conflict = 'name' if 'name' in document_json else 'value'
                error = 'A {0} object with same `{1}` already exists'.format(
                    self.__class__.__name__, conflict)
                raise IntegrityError(error)
        else:
            document_json['_key'] = str(document_json['_key'])
            result = self._get_collection().update(
                document_json, return_new=True)
        arangodoc = result['new']
        return self.schema(strict=True).load(arangodoc).data

    @classmethod
    def list(cls):
        """Lists all objects.

        Returns:
          An arango.cursor.Cursor object.
        """
        colname = cls._collection_name
        objects = cls._db.aql.execute(
            'FOR o IN {0:s} FILTER o.type =~ @type RETURN o'.format(colname),
            bind_vars={
                'type': cls.__name__.lower()
            })

        return cls.load(list(objects))

    @classmethod
    def get(cls, key):
        """Fetches a single object by key.

        Args:
          key: ArangoDB _key value

        Returns:
          A Yeti object."""
        document = cls._get_collection().get(str(key))
        if document:
            return cls.load(document)
        return None

    @classmethod
    def get_or_create(cls, **kwargs):
        """Fetches an object matching dict_ or creates it.

        If an object matching kwargs is found, return the existing object. If
        not, create it and return the newly created object.

        Args:
          **kwargs: Dictionary used to create the object.

        Returns:
          A Yeti object.
        """
        obj = cls(**kwargs)
        try:
            return obj.save()
        except IntegrityError:
            document = list(cls._get_collection().find(kwargs))[0]
            return cls.load(document, strict=True)

    def link_to(self, target, attributes, link_type):
        """Creates a link between two YetiObjects.

        Args:
          target: The YetiObject to link to.
          attributes: A dictionary with attributes to add to the link.
          link_type: The type of link.
        """
        graph = self._db.graph(LINK_TYPE_TO_GRAPH[link_type])
        edge_collection = graph.edge_collection(link_type)
        document = {
            '_from': self._arango_id,
            '_to': target._arango_id,  # pylint: disable=protected-access
            'attributes': attributes,
        }
        return edge_collection.insert(document)

    # pylint: disable=too-many-arguments
    def neighbors(self,
                  link_type,
                  direction='any',
                  include_original=False,
                  hops=1,
                  raw=False):
        """Fetches neighbors of the YetiObject.

        Args:
          link_type: The type of link.
          direction: outbound, inbound, or any.
          hops: The maximum number of nodes to go through (defaults to 1:
              direct neighbors)
        """
        min_depth = 1 if not include_original else None
        graph = self._db.graph(LINK_TYPE_TO_GRAPH[link_type])
        neighbors = graph.traverse(self._arango_id,
                                   direction=direction,
                                   min_depth=min_depth,
                                   max_depth=hops)['vertices']
        if raw:
            return neighbors
        return self.load(neighbors)


    @classmethod
    def filter(cls, args):
        """Search in an ArangoDb collection.

        Search the collection for all objects whose 'value' attribute matches
        the regex defined in the 'value' key of the args dict.

        Args:
            args: A key:value dictionary containing a 'value' or 'name' key
              defining the regular expression to match against.
        """
        colname = cls._collection_name
        conditions = []
        for key in args:
            if key in ['value', 'name', 'type']:
                conditions.append('o.{0:s} =~ @{0:s}'.format(key))
        aql_string = """
        FOR o IN {0:s} FILTER {1:s} RETURN o
        """.format(colname, ' AND '.join(conditions))
        documents = cls._db.aql.execute(aql_string, bind_vars=args)
        yeti_objects = []
        for doc in documents:
            yeti_objects.append(cls.load(doc))
        return yeti_objects

    @classmethod
    def _get_collection(cls):
        """Get the collection corresponding to this Yeti object class.

        Ensures the collection is properly indexed.

        Returns:
          The ArangoDB collection corresponding to the object class.
        """
        collection = cls._db.collection(cls._collection_name)
        for index in cls._indexes:
            collection.add_hash_index(**index)
        return collection
