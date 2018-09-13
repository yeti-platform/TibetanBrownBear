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
    @route('/vocabs/<vocab>/', methods=['GET'])
    def get_vocab(self, vocab):
        """Return defined vocabularies."""
        try:
            v = Setting.get_or_create(name='vocabs')
            return v.get_vocab(vocab)
        except RuntimeException as exception:
            return exception, 400

    @as_json
    @route('/vocabs/<vocab>/', methods=['PUT'])
    def add_value_to_vocab(self, vocab):
        """Set a vocabulary."""
        value = request.json['value']
        try:
            v = Setting.find(name='vocabs')
            v.add_value_to_vocab(vocab, value)
            return v.get_vocab(vocab)
        except RuntimeException as exception:
            return exception, 400

    @as_json
    @route('/vocabs/<vocab>/', methods=['DELETE'])
    def remove_value_from_vocab(self, vocab):
        """Remove a value from a vocab."""
        value = request.json['value']
        v = Setting.find(name='vocabs')
        try:
            v.remove_value_from_vocab(vocab, value)
        except RuntimeException as exception:
            return exception, 400
        return v.get_vocab(vocab)
