"""Detail Yeti's Observable object structure."""

from yeti.core.model.stix import StixCYBOX
from yeti.core.errors import ValidationError, IntegrityError

class Observable(StixCYBOX):

    _collection_name = 'observables'
    type = None
    _type_filter = None
    _indexes = [
        {'fields': ['value'], 'unique': False},
    ]
    _text_indexes = [
        {'fields': ['value']},
    ]

    @classmethod
    def validate_string(cls, string):
        if string:
            return True
        return False

    def is_valid(self):
        try:
            self.normalize()
        except Exception as e:  # pylint: disable=broad-except
            ValidationError('Invalid {0:s} value: {1!r} ({2!r})'.format(
                self.__class__.__name__, self.value, e))
        if not self.validate_string(self.value):
            raise ValidationError('Invalid {0:s} value: {1!r}'.format(
                self.__class__.__name__, self.value))

    def normalize(self):
        pass

    @classmethod
    def guess_type(cls, string):
        """Guesses an observable's type given a string."""
        if string.strip():
            for key, datatype in cls.datatypes.items():
                if key in ['ipv4-addr', 'url', 'domain-name']:
                    if datatype.validate_string(string):
                        return datatype
        return False

    @classmethod
    def get_or_create(cls, **kwargs):
        """Fetches an observable matching the provided kwargs and returns it.

        If an Observable matching kwargs is found, return it. If not, create it
        and return the newly created Observable.

        Args:
          **kwargs: {'value': 'something'} dictionary.

        Returns:
          A Yeti Observable
        """
        obj = cls(value=kwargs['value'])
        obj.normalize()
        try:
            return obj.save()
        except IntegrityError:
            return cls.find(value=obj.value)

    def tag(self, tags, strict=False):
        """Tags an Observable.

        Args:
          tags: A list of strings to tag the Observable with.
          strict: boolean, if True will remove tags that exist in the observable
              but are not provided in "tag"

        """
        if self.tags is None:
            self.tags = []
        now = datetime.utcnow()

        # NOTE: This may be a bit complex for large amounts of tagrefs in a
        # single observable. Maybe use custom DictFields for TagRefs or similar?
        # See https://github.com/marshmallow-code/marshmallow/issues/432
        # for possible solution.

        newtags = list(set(tags))  # dedup tags
        tagref_names = {tagref.name: tagref for tagref in self.tags}

        if strict:  # Remove all tags that are not included in `newtags`
            self.tags = [tag for tag in self.tags if tag.name in newtags]

        for tag in newtags:
            if tag in tagref_names:
                # Tag is found, update .last_seen and .fresh
                tagref_names[tag].last_seen = now
                tagref_names[tag].fresh = True
                continue
            newtag = Tag.get_or_create(name=tag)
            # Tag was not found, create new TagReference
            tagref = TagReference(
                name=newtag.name,
                expiration=now + newtag.default_expiration,
                fresh=True,
                first_seen=now,
                last_seen=now)
            self.tags.append(tagref)

        self.save()
