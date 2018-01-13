"""API resources for interacting with Observables."""

from flask_classful import FlaskView, route
from marshmallow import fields
from webargs.flaskparser import use_args

from yeti.core.types.observable import Observable
from ..helpers import as_json, get_object_or_404

searchargs = {'value': fields.Str(required=True)}

postargs = {
    'key': fields.Str(required=True),
    'value': fields.Str(required=True)
}


class ObservableResource(FlaskView):
    """Class describing resources to manipulate Observable objects."""

    route_base = '/observables/'

    @as_json(Observable)
    def index(self):
        """Return a list of all Observables in the database."""
        return Observable.list()

    @as_json(Observable)
    def get(self, key):
        """Fetch a single observable from the database.
        Args:
            key: The Observable object's primary key.
        Returns:
            A JSON representation of the requested Observable, or a 404 HTTP
            status code if the Observable cannot be found.
        """
        return get_object_or_404(Observable, key)

    @route('/', methods=["POST"])
    @use_args(searchargs)
    @as_json(Observable)
    def post(self, args):
        """Creates a new Observable.

        Args:
            args: key:value dictionary with which to populate the new
            Observable's fields.

        Returns:
            A JSON representation of the saved Observable.
        """
        return Observable.load(args).save()

    @route('/filter/', methods=["POST"])
    @use_args(searchargs)
    @as_json(Observable)
    def filter(self, args):
        """Search the database for Observables with specific fields.

        Args:
            args: A key:value dictionary representing an Observable's
              and its expected values.
        """
        return Observable.filter(args)
