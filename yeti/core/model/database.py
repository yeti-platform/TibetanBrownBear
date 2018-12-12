"""Interface definition for Yeti DB connectors."""


from marshmallow.exceptions import ValidationError as MarshmallowValidationError

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
    _text_indexes = []
    datatypes = {}

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.is_valid()

    def __repr__(self):
        return '<{type:s}({key!r})>'.format(
            type=self.__class__.__name__,
            key=self.value if hasattr(self, 'value') else self.name)

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

    @classmethod
    def load_object_from_type(cls, obj, strict=False):
        objtype = cls.get_final_datatype(obj)
        return objtype.schema(strict=strict).load(obj).data

    @classmethod
    def get_final_datatype(cls, args):
        subclass = cls
        if 'type' in args:
            if args['type'] not in cls.datatypes:
                raise ValidationError(
                    '"{0:s}" not in acceptable datatypes ({1!r})'.format(
                        args['type'], cls.datatypes))
            subclass = cls.datatypes[args['type']]
        return subclass

    def is_valid(self):
        return True


class YetiSchema(ArangoYetiSchema):
    """Generic (de)serialization marshmallow.Schema object for Yeti objects."""

    # pylint: disable=arguments-differ
    def handle_error(self, exc, data):
        """Log and raise our custom exception when (de)serialization fails."""
        error_dict = exc.messages
        if '_schema' in error_dict:
            error_dict = {}
            for idx, error in enumerate(exc.messages['_schema']):
                error_dict[error] = data[idx]
        raise ValidationError(exc.messages)
