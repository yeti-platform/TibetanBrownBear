import click
# import requests

# from yeti.common.config import yeti_config
from yeti.core.model.settings import setting

# pylint: disable=line-too-long
@click.command()
@click.option('--vocab_filter', help='Filter on vocabs to add', type=click.STRING)
def vocab_import(vocab_filter):
    vocabs = setting.Setting.get_or_create(name='vocabs')
    for name, vocab in VOCABS.items():
        if vocab_filter and vocab_filter not in name:
            continue
        vocabs.set_vocab(name, vocab)

STIX_MALWARE_LABEL_OV = [
    'adware',
    'backdoor',
    'bot',
    'ddos',
    'dropper',
    'exploit-kit',
    'keylogger',
    'ransomware',
    'remote-access-trojan',
    'resource-exploitation',
    'rogue-security-software',
    'rootkit',
    'screen-capture',
    'spyware',
    'trojan',
    'virus',
    'worm'
]

STIX_ATTACK_RESOURCE_LEVEL_OV = [
    'individual',
    'club',
    'contest',
    'team',
    'organization',
    'government'
]



VOCABS = {
    'malware-label-ov': STIX_MALWARE_LABEL_OV,
    'attack-resource-level-ov': STIX_ATTACK_RESOURCE_LEVEL_OV
}
