"""Commands to interact with Yara rules stored in Yeti."""

import os

import click

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

    paths = [path]
    max_path_len = 0
    if recurse:
        print('Recursing on directory {0:s}'.format(path))
        paths = []
        for root, _, files in os.walk(path):
            for filename in files:
                full_path = os.path.join(root, filename)
                paths.append(full_path)
                if len(full_path) > max_path_len:
                    max_path_len = len(full_path)

    results = []
    max_ruleid_len = 0
    for rule in yara_rules:
        for filename in paths:
            matches = rule.compiled_pattern.match(filename)
            if matches:
                if len(rule.name) > max_ruleid_len:
                    max_ruleid_len = len(rule.name + rule.id)
                results.append((filename, rule, matches))

    if not results:
        print('No matches found')
        exit()

    print('Found {0:d} matches!'.format(len(results)))
    print('{0:s}   {1:s}   {2:s}'.format(
        'Filename'.ljust(max_path_len), 'ID'.ljust(max_ruleid_len + 3), 'Details' if verbose else ''))
    print('{0:s}   {1:s}   {2:s}'.format(
        '='.ljust(max_path_len, '='), '='.ljust(max_ruleid_len + 3, '='), '='*10 if verbose else ''))
    for filename, rule, result_list in results:
        for result in result_list:
            print('{0:s}   {1:s}   {2!s}'.format(
                filename.ljust(max_path_len),
                '{} ({})'.format(rule.name, rule.id).ljust(max_ruleid_len),
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
