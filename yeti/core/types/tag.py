"""Detail the Yeti's Tag object structure."""

import re
from datetime import datetime

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from yeti.core.model.fields import RealDateTime, RealTimeDelta
from ..model.database import YetiObject, YetiSchema


class TagSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Tag objects."""
    name = fields.String(required=True)
    count = fields.Integer(required=True, default=0)
    created_at = RealDateTime()
    default_expiration = RealTimeDelta()

    @post_load
    def load_tag(self, data):
        """Load a Tag object from its JSON representation.

        Returns:
          The created Tag object.
        """
        tag = Tag(**data)
        tag.normalize()
        return tag


class Tag(YetiObject):
    """Tag object.

    Attributes:
      name: Name of the tag.
      count: Count of tags in the database.
      created_at: timestamp when the Tag object was first created.
      default_expiration: Time after which the tag should expire on an Observable.
    """

    _collection_name = 'tags'
    _schema = TagSchema

    id = None
    name = None
    # count = None
    created_at = None
    default_expiration = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Tag({name!r})>'.format(name=self.name)

    def normalize(self):
        initial = self.name
        self.name = re.sub(r'[^a-z0-9\-_ ]', '', self.name.lower())
        self.name = re.sub(' ', '_', self.name)
        if not self.name:
            raise ValidationError('Tag name "{0:s}" is invalid'.format(
                initial
            ))


class TagReferenceSchema(YetiSchema):
    """(De)serialization marshmallow.Schema for Tag objects."""
    name = fields.String(required=True)
    expiration = fields.DateTime(required=True)
    fresh = fields.Boolean()
    first_seen = fields.DateTime(default=datetime.utcnow)
    last_seen = fields.DateTime(default=datetime.utcnow)

    name = None
    expiration = None
    fresh = None
    first_seen = None
    last_seen = None

    @post_load
    def load_tag(self, data):
        """Load a TagReference object from its JSON representation.

        Returns:
          The created TagReference object.
        """
        return TagReference(**data)

class TagReference(YetiObject):
    """Reference to a Tag object. This will be attached to Observables.
    Attributes:
      name: Name of the tag to Reference
      expiration: Date after which the tag will expire.
      fresh: Boolean indicating whether the tag has expired or not.
      first_seen: Date on which the observable was first tagged.
      last_seen: Date on which the observable was last tagged.
    """

    name = None
    expiration = None
    fresh = None
    first_seen = None
    last_seen = None

    _schema = TagReferenceSchema

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
