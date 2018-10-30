"""API resources for interacting with Entities."""
from marshmallow import fields

from yeti.core.relationships import BaseRelationship
from .generic import GenericResource


class RelationshipResource(GenericResource):
    """Class describing resources to manipulate BaseRelationship objects."""

    route_base = '/relationships/'
    resource_object = BaseRelationship

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }
