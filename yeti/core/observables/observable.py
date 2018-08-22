"""Detail Yeti's Observable object structure."""

from yeti.core.model.stix import StixCYBOX
from yeti.core.errors import ValidationError, IntegrityError

class Observable(StixCYBOX):

    _collection_name = 'observables'
    type = None
    _type_filter = None
    _indexes = [
        {'fields': ['value'], 'unique': True},
    ]
    _text_indexes = [
        {'fields': ['value']},
    ]

    def is_valid(self):
        try:
            self.normalize()
        except Exception as e:  # pylint: disable=broad-except
            ValidationError('Invalid {0:s} value: {1!r} ({2!r})'.format(
                self.__class__.__name__, self.value, e))
        if not self.validate_string(self.value):
            raise ValidationError('Invalid {0:s} value: {1!r}'.format(
                self.__class__.__name__, self.value))

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
