# pylint: disable=unused-argument
"""Tests for Yeti vocabs"""
import pytest

from yeti.core.model.settings.vocabs import Vocabs
from yeti.core.model.settings.setting import Setting

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_create_vocab_setting():
    """Tests that Vocab settings can be created."""
    vocab = Setting.get_or_create(name='my_vocab', type='vocab')
    vocab_ = Vocabs.get(vocab.id)
    assert vocab_ is not None
    assert vocab.id == vocab_.id
    assert vocab_.name == 'my_vocab'

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_get_vocab_setting():
    """Tests that a vocab setting can be saved and has correct type."""
    vocab = Setting.find(name='malware-label-ov')
    assert isinstance(vocab, Vocabs)

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_set_vocab():
    """Tests that a vocab can be set for a given field."""
    vocab = Setting.find(name='malware-label-ov')
    vocab.set_vocab(['toto'])
    vocablist = vocab.get_vocab()
    assert vocablist == ['toto']

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_vocab():
    """Tests that vocabs can be added to a vocab list for a given field."""
    vocab = Setting.find(name='malware-label-ov')
    vocab.set_vocab(['banker'])
    vocab.add_value_to_vocab('trojan')
    vocablist = vocab.get_vocab()
    assert vocablist == sorted(['banker', 'trojan'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_vocab():
    """Tests that a vocab can be removed from a vocab list for a given field."""
    vocab = Setting.find(name='malware-label-ov')
    vocab.set_vocab(sorted(['banker', 'trojan']))
    vocab.remove_value_from_vocab('trojan')
    vocablist = vocab.get_vocab()
    assert vocablist == ['banker']

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_filter_vocab():
    """Tests that a vocab list for a given list can be filtered."""
    vocab = Setting.find(name='malware-label-ov')
    vocab.set_vocab(sorted(['banker', 'trojan']))
    assert vocab.filter_values_vocab('tro') == ['trojan']
