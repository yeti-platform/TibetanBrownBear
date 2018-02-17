"""API resources for interacting with Entities."""
from marshmallow import fields

from yeti.core.entities.entity import Entity
from .generic import GenericResource


class EntityResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/entities/'
    resource_object = Entity

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }
