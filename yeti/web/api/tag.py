"""API resources for interacting with Tags."""
from marshmallow import fields

from yeti.core.observables.tag import Tag
from .generic import GenericResource


class TagResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/tags/'
    resource_object = Tag

    searchargs = {
        'name': fields.Str(required=True),
    }
