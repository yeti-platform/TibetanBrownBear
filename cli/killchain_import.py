import json
import os
import click

from yeti.core.model.settings import setting

KILLCHAIN_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'killchains.json')
# pylint: disable=line-too-long
@click.command()
@click.option('--killchain_filter', help='Filter on killchains to add', type=click.STRING)
def killchain_import(killchain_filter):
    killchains = setting.Setting.get_or_create(name='killchains')
    with open(KILLCHAIN_FILE) as vocabsfile:
        for killchain in json.load(vocabsfile):
            if killchain_filter and killchain_filter not in killchain['name']:
                continue
            killchains.set_phases(killchain['name'], killchain['phases'])
