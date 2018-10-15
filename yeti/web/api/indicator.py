"""API resources for interacting with Entities."""
from marshmallow import fields
from flask_classful import route
from flask import request

from yeti.core.indicators.indicator import Indicator
from yeti.core.errors import YetiSTIXError, ValidationError
from .generic import GenericResource
from ..helpers import as_json, get_object_or_404, decode_object


class IndicatorResource(GenericResource):
    """Class describing resources to manipulate Indicator objects."""

    route_base = '/indicators/'
    resource_object = Indicator

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    @as_json
    @route('/<id>/', methods=['PUT'])
    def put(self, id):  # pylint: disable=redefined-builtin
        """Updates a STIX SDO object.

        Args:
            id: The object's primary ID.

        Returns:
            A JSON representation of the requested object, or a 404 HTTP
            status code if the object cannot be found.
        """
        # Remove unupdatable fields (created, id, type) from the request JSON
        # Also remove the 'modified' field since we want STIX to change the
        # timestamp
        update_dict = request.get_json()
        update_dict.pop('created', None)
        update_dict.pop('id', None)
        update_dict.pop('type', None)
        update_dict.pop('modified', None)
        try:
            obj = get_object_or_404(self.resource_object, id)
            return obj.update(update_dict)
        except (YetiSTIXError, ValidationError) as err:
            return err, 400

    @as_json
    @route('/match/', methods=['POST'])
    def match(self):
        """Matches a series of binary objects against indicators."""
        objects = request.get_json()
        all_indicators = Indicator.list()
        matches = []
        for obj in objects:
            decoded = decode_object(obj)
            for indicator in all_indicators:
                match = indicator.match(decoded)
                if match:
                    matches.append(match)
        return matches
