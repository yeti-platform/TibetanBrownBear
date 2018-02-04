"""API resources for interacting with Observables."""

from flask import request
from flask_classful import FlaskView, route
from marshmallow import fields
from webargs.flaskparser import parser

from yeti.core.types.observable import Observable
from ..helpers import as_json, get_object_or_404

searchargs = {
    'value': fields.Str(required=True),
    'type': fields.Str(),
}

postargs = {
    'key': fields.Str(required=True),
    'value': fields.Str(required=True),
}


class ObservableResource(FlaskView):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'

    @as_json(Observable)
    def index(self):
        """Return a list of all Observables in the database."""
        return Observable.list()

    @as_json(Observable)
    # pylint: disable=W0622
    def get(self, id):
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
        return Observable.load(args).save()

    @as_json(Observable)
    @route('/<id>/', methods=["PUT"])
    # pylint: disable=W0622
    def put(self, id):
        """Creates a new Observable.

        Args:
            id: The Observable object's primary ID.

        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        args = parser.parse(searchargs, request)
        observable = get_object_or_404(Observable, id)
        return observable.update(args).save()


    @route('/filter/', methods=["POST"])
    @as_json(Observable)
    def filter(self):
        """Search the database for Observables with specific fields."""
        args = parser.parse(searchargs, request)
        return Observable.filter(args)
