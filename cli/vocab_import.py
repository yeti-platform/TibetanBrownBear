import json
import os
import click

from yeti.core.model.settings import setting

VOCABS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vocabs.json')
# pylint: disable=line-too-long
@click.command()
@click.option('--vocab_filter', help='Filter on vocabs to add', type=click.STRING)
def vocab_import(vocab_filter):
    vocabs = setting.Setting.get_or_create(name='vocabs')
    with open(VOCABS_FILE) as vocabsfile:
        for vocab in json.load(vocabsfile):
            if vocab_filter and vocab_filter not in vocab['name']:
                continue
            values = [v['value'] for v in vocab['values']]
            vocabs.set_vocab(vocab['name'], values)
