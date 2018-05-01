"""API resources for interacting with Observables."""
from flask import request
from marshmallow import fields
from flask_classful import route
from webargs.flaskparser import parser

from yeti.core.types.observable import Observable
from yeti.core.errors import GenericYetiError, ValidationError
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
        obj.tag(args['tags'])
        return obj

    @as_json
    @route('/<id>/', methods=['PUT'])
    def put(self, id):  # pylint: disable=redefined-builtin
        """Updates an Observable.

        If tags are provided in the request, they will individually be applied
        to the observable in question.

        Args:
            id: The Observable's primary ID.

        Returns:
            A JSON representation of the Observable, a 404 HTTP status code if
            the Observable cannot be found, or a 400 HTTP status code if the
            request could not be parsed.
        """
        try:
            obj = get_object_or_404(self.resource_object, id)
            dumped = obj.dump()
            request_json = request.get_json()
            tags = request_json.pop('tags', [])
            dumped.update(request_json)
            saved_object = self.resource_object.load(dumped).save()
            saved_object.tag(tags, strict=True)
            return saved_object

        except GenericYetiError as err:
            import traceback
            traceback.print_exc()
            return err, 400
