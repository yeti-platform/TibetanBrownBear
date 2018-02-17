"""API resources for interacting with Indicators."""
from marshmallow import fields

from yeti.core.indicators.indicator import Indicator
from .generic import GenericResource


class IndicatorResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/indicators/'
    resource_object = Indicator

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }
