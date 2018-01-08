"""API resources for interacting with Observables."""

from flask_classful import FlaskView, route
from flask import jsonify
from marshmallow import fields, Schema
from webargs.flaskparser import use_args, use_kwargs

from core.types.observable import Observable

searchargs = {
    'value': fields.Str(required=True)
}

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
        return jsonify(Observable._schema(many=True).dump(
            Observable.list()).data)

    def get(self, key):
        obs = Observable.get(key)
        if not obs:
            return "", 404
        return jsonify(Observable._schema().dump(obs).data)

    @route('/', methods=["POST"])
    @use_args(searchargs)
    def post(self, args):
        observable = Observable._schema().load(args).data
        return jsonify(Observable._schema().dump(observable.save()).data)

    @use_args(searchargs)
    @route('/filter/', methods=["POST"])
    def filter(self, args):
        return jsonify(Observable._schema(many=True).dump(Observable.filter(args)).data)
