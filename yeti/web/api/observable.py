"""API resources for interacting with Observables."""
from flask import request
from marshmallow import fields
from flask_classful import route
from webargs.flaskparser import parser

from yeti.core import analysis
from yeti.core.observables.observable import Observable
from yeti.web.helpers import as_json, get_object_or_404
from yeti.core.errors import GenericYetiError
from .generic import GenericResource


class ObservableResource(GenericResource):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'
    resource_object = Observable

    searchargs = {
        'value': fields.Str(required=True),
        'type': fields.Str(),
    }

    fulltext_searchargs = {
        'keywords': fields.List(fields.String(), required=True),
    }

    tagargs = {
        'tags': fields.List(fields.String(), required=True),
    }

    matchargs = {
        'observables': fields.List(fields.String(), required=True)
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
        to the observable in question. Fields not part of the observable schema
        will be ignored.

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
            tags = []
            for tag in request_json.pop('tags', []):
                tags.append(tag['name'] if isinstance(tag, dict) else tag)
            dumped.update(request_json)
            saved_object = self.resource_object.load(dumped).save()
            saved_object.tag(tags, strict=True)
            return saved_object

        except GenericYetiError as err:
            import traceback
            traceback.print_exc()
            return err, 400

    @as_json
    @route('/match', methods=['POST'])
    def match(self):
        query = parser.parse(self.matchargs, request)
        return analysis.match_observables(query['observables'])
