from flask_classful import FlaskView, route
from flask import request

from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException
from ..helpers import as_json

class SettingsResource(FlaskView):
    """Class describing resources to manipulate Yeti settings."""

    route_base = '/settings/'
    resource_object = Setting
    searchargs = None
    fulltext_searchargs = None

    @as_json
    @route('/vocabs/<field>/', methods=['GET'])
    def get_vocab_for_field(self, field):
        """Return defined vocabularies for a field."""
        v = Setting.find(name='vocabs')
        return v.get_vocab_for_field(field)

    @as_json
    @route('/vocabs/<field>/', methods=['PUT'])
    def add_value_to_field_vocab(self, field):
        """Return defined vocabularies for a field."""
        value = request.json['value']
        v = Setting.find(name='vocabs')
        v.add_value_to_field_vocab(field, value)
        return v.get_vocab_for_field(field)

    @as_json
    @route('/vocabs/<field>/', methods=['DELETE'])
    def remove_value_from_field_vocab(self, field):
        """Return defined vocabularies for a field."""
        value = request.json['value']
        v = Setting.find(name='vocabs')
        try:
            v.remove_value_from_field_vocab(field, value)
        except RuntimeException as exception:
            return exception, 400
        return v.get_vocab_for_field(field)
