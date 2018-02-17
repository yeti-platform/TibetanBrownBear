"""API resources for interacting with Observables."""
from marshmallow import fields
# from flask import request
# from flask_classful import route
# from webargs.flaskparser import parser

from yeti.core.entities.entity import Entity
from .generic import GenericResource
# from ..helpers import as_json, get_object_or_404


class EntityResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/entities/'
    resource_object = Entity

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    tagargs = {
        'tags': fields.List(fields.String(), required=True),
    }
