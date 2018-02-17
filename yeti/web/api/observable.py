"""API resources for interacting with Observables."""
from marshmallow import fields
from flask import request
from flask_classful import route
from webargs.flaskparser import parser

from yeti.core.types.observable import Observable
from yeti.core.errors import ValidationError
from .generic import GenericResource
from ..helpers import as_json, get_object_or_404

@parser.error_handler
def handle_args(err):
    raise ValidationError(err.messages)

class ObservableResource(GenericResource):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'
    resource_object = Observable

    searchargs = {
        'value': fields.Str(required=True),
        'type': fields.Str(),
    }

    tagargs = {
        'tags': fields.List(fields.String(), required=True),
    }

    @as_json
    @route('/<id>/tag', methods=['POST'])
    def tag(self, id):  # pylint: disable=redefined-builtin
        """Updates a given object.

        Args:
            id: The object's primary ID.

        Returns:
            A JSON representation of the requested object, or a 404 HTTP
            status code if the object cannot be found.
        """
        args = parser.parse(self.tagargs, request)
        obj = get_object_or_404(self.resource_object, id)
        for tag in args['tags']:
            obj.tag(tag)
        return obj
