"""Populate Yeti's database with pre-defined killchains."""
import json
import os
import click

from taxii2client import Collection
from stix2 import TAXIICollectionSource, Filter

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

MITRE_TACTICS_URL = "https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/"
@click.command()
def mitre_tactics_import():
    collection = Collection(MITRE_TACTICS_URL)
    tc_source = TAXIICollectionSource(collection)
    kc = KillChains.get_or_create(name='mitre-attack')
    kc.description = 'The MITRE ATT&CK tactics are represented as kill-chains in STIX2'
    kc.save()
    for item in tc_source.query(Filter('type', '=', 'x-mitre-tactic')):
        print(f'Adding {item["x_mitre_shortname"]}')
        kc.add_phase_to_killchain({
            'name': item['x_mitre_shortname'],
            'description': item['description']
        })
