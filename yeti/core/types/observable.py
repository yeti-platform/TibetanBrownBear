"""Detail the Yeti's Observable object structure."""

from datetime import datetime

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from ..model.database import YetiObject, YetiSchema
from .tag import Tag, TagReference, TagReferenceSchema

class ObservableSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Observable objects."""
    value = fields.String(required=True)
    type = fields.String()
    tags = fields.Nested(TagReferenceSchema, many=True, allow_none=True)

    @post_load
    def load_observable(self, data):
        """Load an Observable object from its JSON representation.

        @post_load means this will be called after eath marshmallow.load call.

        Returns:
          The Observable object.
        """
        datatype = DATATYPES[data['type']]
        object_ = datatype(**data)
        object_.normalize()
        return object_


class Observable(YetiObject):
    """Observable Yeti object.

    Attributes:
      key: Database primary key
      value: Observable value
    """

    _collection_name = 'observables'
    _indexes = [
        {'fields': ['value'], 'unique': True},
    ]
    _schema = ObservableSchema

    id = None
    value = None
    type = 'observable'
    tags = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.is_valid()

    def __repr__(self):
        return '<{type:s}(value={value!r})>'.format(
            type=self.__class__.__name__,
            value=self.value)

    def is_valid(self):
        if self.value is not None:
            return True
        raise ValidationError

    def normalize(self):
        pass

    def tag(self, tag):
        tag = Tag(name=tag).save()
        if self.tags is None:
            self.tags = []
        now = datetime.utcnow()
        reference = TagReference(
            name=tag.name,
            expiration=now + tag.default_expiration,
            fresh=True,
            first_seen=now,
            last_seen=now)

        self.tags.append(reference)
        self.save()

DATATYPES = {
    'observable': Observable,
}
