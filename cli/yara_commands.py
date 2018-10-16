"""Commands to interact with Yara rules stored in Yeti."""

import os

import click
import yara

from yeti_python_api import api

@click.command()
@click.option('--recurse', help='Recurse in directory', is_flag=True, default=False)  # pylint: disable=line-too-long
@click.option('--verbose', help='Display match details', is_flag=True, default=False)  # pylint: disable=line-too-long
@click.option('--name_filter', help='Filter indicators by name', type=click.STRING, default='')  # pylint: disable=line-too-long
@click.argument('path', type=click.STRING)
def yara_scan(path, name_filter, verbose, recurse):
    """Scan a local file or directory using Yara rules from the Yeti server."""
    if not os.path.exists(path):
        print('Error: {0:s} was not found'.format(path))
        exit(-1)
    yara_rules = api.filter_indicators(name_filter, 'x-yara')
    for rule in yara_rules:
        results = rule.compiled_pattern.match(path)
        if not results:
            print('No matches found.')
            exit()
        print('Found {0:d} matches!'.format(len(results)))
        print('{0:<20s} {1:<55s} {2:s}'.format(
            'Name', 'ID', 'Details' if verbose else ''))
        print('{0:<20s} {1:<55s} {2:s}'.format(
            '='*10, '='*10, '='*10 if verbose else ''))
        for result in results:
            print('{0:<20s} {1:<55s} {2!s}'.format(
                rule.name,
                rule.id,
                result.strings if verbose else ''
            ))


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
