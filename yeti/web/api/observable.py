"""API resources for interacting with Observables."""

from flask import request
from flask_classful import FlaskView, route
from marshmallow import fields
from webargs.flaskparser import parser

from yeti.core.errors import ValidationError
from yeti.core.types.observable import Observable
from ..helpers import as_json, get_object_or_404

searchargs = {
    'value': fields.Str(required=True),
    'type': fields.Str(),
}

tagargs = {
    'tags': fields.List(fields.String(), required=True),
}


class ObservableResource(FlaskView):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'

    @as_json(Observable)
    def index(self):
        """Return a list of all Observables in the database."""
        return Observable.list()

    @as_json(Observable)
    def get(self, id):  # pylint: disable=redefined-builtin
        """Fetch a single observable from the database.

        Args:
            id: The Observable object's primary ID.

        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        return get_object_or_404(Observable, id)

    @route('/', methods=["POST"])
    @as_json(Observable)
    def post(self):
        """Creates a new Observable.

        Returns:
            A JSON representation of the saved Observable.
        """
        args = parser.parse(searchargs, request)
        try:
            obs = Observable.load(args).save()
        except ValidationError as err:
            return err, 400
        return obs

    @as_json(Observable)
    @route('/<id>/', methods=["PUT"])
    def put(self, id):  # pylint: disable=redefined-builtin
        """Updates a given Observable.

        Args:
            id: The Observable object's primary ID.

        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        args = parser.parse(searchargs, request)
        observable = get_object_or_404(Observable, id)
        return observable.update(args).save()

    @as_json(Observable)
    @route('/<id>/tag', methods=['POST'])
    def tag(self, id):  # pylint: disable=redefined-builtin
        """Updates a given Observable.

        Args:
            id: The Observable object's primary ID.

        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        args = parser.parse(tagargs, request)
        observable = get_object_or_404(Observable, id)
        for tag in args['tags']:
            observable.tag(tag)
        return observable


    @route('/filter/', methods=["POST"])
    @as_json(Observable)
    def filter(self):
        """Search the database for Observables with specific fields."""
        args = parser.parse(searchargs, request)
        return Observable.filter(args)
