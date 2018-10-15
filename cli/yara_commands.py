"""Commands to interact with Yara rules stored in Yeti."""

import os

import click
import yara

from yeti_python_api import api

@click.command()
@click.option('--name_filter', help='Filter indicators by name', type=click.STRING, default='')  # pylint: disable=line-too-long
@click.option('--recurse', help='Recurse over directories found', type=click.BOOL)  # pylint: disable=line-too-long
@click.argument('path', type=click.STRING)
def yara_scan(path, recurse, name_filter):
    """Scan a local file or directory using Yara rules from the Yeti server."""
    if not os.path.exists(path):
        print('Error: {0:s} was not found'.format(path))
        exit(-1)
    yara_rules = api.filter_indicators(name_filter, 'x-yara')
    for rule in yara_rules:
        # TODO: do something with this, like actually scan the file
        print(rule.name)


@click.command()
@click.option('--name_filter', help='Filter indicators by name', type=click.STRING, default='')  # pylint: disable=line-too-long
@click.argument('path', type=click.STRING)
def dump_yara_rules(path, name_filter):
    """Dump existing Yara rules to files in a local directory."""
    if not os.path.exists(path):
        print('Error: {0:s} was not found'.format(path))
        exit(-1)
    yara_rules = api.filter_indicators(name_filter, 'x-yara')
    choice = input('About to dump {0:d} Yara rules to "{1:s}"\n'
                   'Continue? [Y/n] '.format(len(yara_rules), path))
    if not choice.lower() in ['y', 'yes', '']:
        exit()
    for rule in yara_rules:
        filename = (rule.name + '.yara').lower()
        with open(filename, 'w') as output:
            output.write(rule.pattern)
        print('[+] Wrote rule "{0:s}" to {1:s}'.format(rule.name, filename))
