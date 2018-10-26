"""API resources for interacting with Entities."""
from marshmallow import fields
from flask_classful import route
from flask import request

from yeti.core.relationships import BaseRelationship
from yeti.core.errors import YetiSTIXError
from .generic import GenericResource
from ..helpers import as_json, get_object_or_404


class RelationshipResource(GenericResource):
    """Class describing resources to manipulate BaseRelationship objects."""

    route_base = '/relationships/'
    resource_object = BaseRelationship

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }