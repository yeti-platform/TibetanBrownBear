from flask_classful import FlaskView, route
from flask import request

from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException
from ..helpers import as_json, auth_required

class SettingsResource(FlaskView):
    """Class describing resources to manipulate Yeti settings."""

    route_base = '/settings/'
    resource_object = Setting
    searchargs = None
    fulltext_searchargs = None

    @as_json
    @route('/vocabs/<vocab>/', methods=['GET'])
    @auth_required
    def get_vocab(self, vocab):
        """Return defined vocabularies."""
        try:
            v = Setting.get_or_create(name='vocabs')
            return v.get_vocab(vocab)
        except RuntimeException as exception:
            return exception, 400

    @as_json
    @route('/vocabs/<vocab>/', methods=['PUT'])
    @auth_required
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
    @auth_required
    def remove_value_from_vocab(self, vocab):
        """Remove a value from a vocab."""
        value = request.json['value']
        v = Setting.find(name='vocabs')
        try:
            v.remove_value_from_vocab(vocab, value)
        except RuntimeException as exception:
            return exception, 400
        return v.get_vocab(vocab)

    @as_json
    @route('/killchains/<killchain>/', methods=['GET'])
    @auth_required
    def get_killchain(self, killchain):
        """Return defined killchains."""
        try:
            v = Setting.get_or_create(name='killchains')
            return v.get_killchain(killchain)
        except RuntimeException as exception:
            return exception, 400

    @as_json
    @route('/killchains/<killchain>/', methods=['PUT'])
    @auth_required
    def add_phase_to_killchain(self, killchain):
        """Set phases for a killchain."""
        phase = request.json['phase']
        try:
            kc = Setting.find(name='killchains')
            kc.add_phase_to_killchain(killchain, phase)
            return kc.get_killchain(killchain)
        except RuntimeException as exception:
            return exception, 400

    @as_json
    @route('/killchains/<killchain>/', methods=['DELETE'])
    @auth_required
    def remove_phase_from_killchain(self, killchain):
        """Remove a phase from a killchain."""
        phase = request.json['phase']
        kc = Setting.find(name='killchains')
        try:
            kc.remove_phase_from_killchain(killchain, phase)
        except RuntimeException as exception:
            return exception, 400
        return kc.get_killchain(killchain)
