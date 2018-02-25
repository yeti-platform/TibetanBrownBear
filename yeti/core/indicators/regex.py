"""Detail Yeti's regular expression indicator structure."""

import re

from marshmallow import fields, post_load

from yeti.core.errors import ValidationError
from .indicator import Indicator, IndicatorSchema


class RegexSchema(IndicatorSchema):
    """(De)serialization marshmallow.Schema for Malware objects."""
    pattern = fields.String(required=True, allow_none=True)

    @post_load
    def load_regular_expression(self, regex_object):
        """Load a Regex object from its JSON representation.

        Returns:
          The Regex object.
        """
        if regex_object.pattern:
            regex_object.compiled_regex = re.compile(regex_object.pattern)
        return regex_object


class Regex(Indicator):
    """Yara rule Yeti object.

    Attributes:
      family: list(str), the families this malware belongs to.
    """

    schema = RegexSchema
    _collection_name = 'indicators'

    type = 'indicator.regex'
    pattern = ''
    compiled_regex = None

    def is_valid(self):
        Indicator.is_valid(self)
        if not isinstance(self.pattern, str):
            raise ValidationError('.pattern must be str')
        try:
            re.compile(self.pattern)
        except re.error as err:
            raise ValidationError(
                'Could not compile regular expression: {0:s}'.format(str(err)))
        return True

    def match(self, obj):
        """Matches the Regex's compiled regular expression against a string.

        Args:
          obj: A string to match the regex on.

        Returns:
          The match.group() if there is a match, None otherwise.
        """
        match = self.compiled_regex.search(obj)
        if match:
            return match.group()
        return None

Indicator.datatypes[Regex.type] = Regex
