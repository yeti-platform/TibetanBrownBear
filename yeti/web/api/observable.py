"""API resources for interacting with Observables."""

from flask_classful import FlaskView, route
from flask import jsonify
from marshmallow import fields
from webargs.flaskparser import use_args

from core.types.observable import Observable

searchargs = {'value': fields.Str(required=True)}

postargs = {
    'key': fields.Str(required=True),
    'value': fields.Str(required=True)
}


class ObservableResource(FlaskView):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'

    # NOTE: This "jsonify(Observable._schema().dump().data" pattern is not
    # sustainable We should use some kind of decorator to always return JSON
    # like what flask-apiscpec does.

    # NOTE: implement the load and dump methods in the ArangoYetiConnector
    # method so we can call Observable.load and Observable.dump

    def index(self):
        """Return a list of all Observables in the database."""
        return jsonify(
            Observable._schema(many=True).dump(Observable.list()).data)

    def get(self, key):
        """Fetch a single observable from the database.
        Args:
            key: The Observable object's primary key.
        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        obs = Observable.get(key)
        if not obs:
            return "", 404
        return jsonify(Observable._schema().dump(obs).data)

    @route('/', methods=["POST"])
    @use_args(searchargs)
    def post(self, args):
        """Creates a new Observable.

        Args:
            args: key:value dictionary with which to populate the new
            Observable's fields.

        Returns:
            A JSON representation of the saved Observable.
        """
        observable = Observable._schema().load(args).data
        return jsonify(Observable._schema().dump(observable.save()).data)

    @use_args(searchargs)
    @route('/filter/', methods=["POST"])
    def filter(self, args):
        """Search the database for Observables with specific fields.

        Args:
            args: A key:value dictionary representing an Observable's
              and its expected values.
        """
        return jsonify(
            Observable._schema(many=True).dump(Observable.filter(args)).data)
