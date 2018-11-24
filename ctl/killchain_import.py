"""Populate Yeti's database with pre-defined killchains."""
import json
import os
import click

from yeti.core.model.settings import setting
from yeti.core.model.settings.killchains import KillChains

KILLCHAIN_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'killchains.json')
# pylint: disable=line-too-long
@click.command()
@click.option('--killchain_filter', help='Filter on killchains to add', type=click.STRING)
def killchain_import(killchain_filter):
    with open(KILLCHAIN_FILE) as vocabsfile:
        for killchain in json.load(vocabsfile):
            if killchain_filter and killchain_filter not in killchain['name']:
                continue
            phases = killchain.pop('phases')
            kc = KillChains(**killchain)
            kc.set_phases(phases)
