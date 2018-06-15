"""API resources for interacting with Indicators."""
from flask import request
from marshmallow import fields
from flask_classful import route
from webargs.flaskparser import parser

from yeti.core.indicators.indicator import Indicator
from .generic import GenericResource
from ..helpers import as_json


class IndicatorResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/indicators/'
    resource_object = Indicator

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    matchargs = {
        'object': fields.Raw(required=True),
        'filter': fields.Dict(),
    }

    @as_json
    @route('/match', methods=['POST'])
    def match(self):  # pylint: disable=redefined-builtin
        """Matches an object against a set of indicators.

        Returns:
            A JSON representation of the match,
            A 404 (Not Found) HTTP response if no indicators matched the filter.
        """
        args = parser.parse(self.matchargs, request)
        if 'filter' in args:
            indicators = Indicator.filter(args)
        else:
            indicators = Indicator.list()

        if not indicators:
            return '', 404

        matches = []
        for indicator in indicators:
            match = indicator.match(args['object'])
            if match:
                matches.append(match)

        return matches, 200
