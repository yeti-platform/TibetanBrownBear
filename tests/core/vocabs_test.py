# pylint: disable=unused-argument
"""Tests for Yeti settings"""
import pytest

from yeti.core.model.settings.vocabs import Vocabs
from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_get_vocab_setting():
    """Tests that a vocab setting can be saved and has correct type."""
    vocab = Setting.find(name='vocabs')
    assert isinstance(vocab, Vocabs)

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_set_vocab():
    """Tests that a vocab can be set for a given field."""
    vocab = Setting.find(name='vocabs')
    vocab.set_vocab_for_field('Malware.type', ['banker', 'other'])
    vocablist = vocab.get_vocab_for_field('Malware.type')
    assert vocablist == ['banker', 'other']

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_add_vocab():
    """Tests that vocabs can be added to a vocab list for a given field."""
    vocab = Setting.find(name='vocabs')
    vocab.set_vocab_for_field('Malware.type', ['banker'])
    vocab.add_value_to_field_vocab('Malware.type', 'trojan')
    vocablist = vocab.get_vocab_for_field('Malware.type')
    assert vocablist == sorted(['banker', 'trojan'])

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_remove_vocab():
    """Tests that a vocab can be removed from a vocab list for a given field."""
    vocab = Setting.find(name='vocabs')
    vocab.set_vocab_for_field('Malware.type', sorted(['banker', 'trojan']))
    vocab.remove_value_from_field_vocab('Malware.type', 'trojan')
    vocablist = vocab.get_vocab_for_field('Malware.type')
    assert vocablist == ['banker']

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_filter_vocab():
    """Tests that a vocab list for a given list can be filtered."""
    vocab = Setting.find(name='vocabs')
    vocab.set_vocab_for_field('Malware.type', sorted(['banker', 'trojan']))
    assert vocab.filter_values_for_field_vocab('Malware.type', 'tro') == ['trojan']

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_wrong_field_raises():
    """Tests that a RuntimeError is raised when getting a noneixstent vocab."""
    vocab = Setting.find(name='vocabs')
    with pytest.raises(RuntimeException):
        vocab.get_vocab_for_field('Notexist')

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_wrong_remove_vocab_raises():
    """Tests that a RuntimeError is raised when getting a noneixstent vocab."""
    vocab = Setting.find(name='vocabs')
    vocab.set_vocab_for_field('Malware.type', sorted(['banker', 'trojan']))
    with pytest.raises(RuntimeException):
        vocab.remove_value_from_field_vocab('Notexist', ['banker'])
    with pytest.raises(RuntimeException):
        vocab.remove_value_from_field_vocab('Malware.type', 'notexist')
