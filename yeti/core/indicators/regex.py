import re

from stix2 import CustomObject, properties


@CustomObject('x-regex', [
    ('labels', properties.StringProperty(required=True)),
    ('name', properties.StringProperty()),
    ('description', properties.StringProperty()),
    ('pattern', properties.StringProperty(required=True)),
    ('valid_from', properties.TimestampProperty(required=True)),
    ('valid_until', properties.TimestampProperty()),
    ('kill_chain_phases', properties.TimestampProperty())
])
class StixRegex():
    def __init__(self, pattern=None, **_):
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError('{0:s} is not a valid regular expression: {1:s}'.format(pattern, str(e)))


class Regex():
    pass
