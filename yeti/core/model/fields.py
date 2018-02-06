from datetime import datetime, timedelta
from marshmallow import fields

import pytz
from dateutil import parser


class RealTimeDelta(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            value = timedelta(hours=24)
        return value.total_seconds()

    def _deserialize(self, value, attr, data):
        return timedelta(seconds=value)

class RealDateTime(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            value = datetime.now(tz=pytz.utc)
        return value.isoformat()

    def _deserialize(self, value, attr, data):
        return parser.parse(value)
