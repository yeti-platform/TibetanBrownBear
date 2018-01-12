"""API resources for interacting with Observables."""

from flask_classful import FlaskView, route
from flask import jsonify
from marshmallow import fields, Schema
from webargs.flaskparser import use_args

testobs = [{'id': 123, 'value': 'yeti.org'}]


class ObservableSchema(Schema):
    class Meta:
        fields = ('id', 'value')

searchargs = {
    "value": fields.Str(required=True)
}


class Observable(FlaskView):
    """Class describing resources to manipulate Observable objects."""

    def get(self, **kwargs):
        print(kwargs)
        return "GETTEST"

    @route('/search', methods=['POST'])
    @use_args(searchargs)
    def search(self, args):
        print (args)
        for o in testobs:
            if args['value'] in o['value']:
                return jsonify(o)

        return ""
