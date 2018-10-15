"""Commands that match strings or file contents server-side."""
import click

from yeti_python_api import api

# pylint: disable=line-too-long
@click.command()
@click.option('--verbose', help='Display match details', type=click.BOOL, default=False)
@click.option('--filename', help='Upload a file to be matched instead.', type=click.STRING)
@click.option('--string', help='String against which to match indicators.', type=click.STRING, default='')
def match(string, filename, verbose):
    """Matches a string or a file's contents against all yeti Indicators."""
    if not (filename or string):
        print('Please provide either a filename or a string to match.')
        exit(-1)
    data = string
    if filename:
        try:
            with open(filename, 'rb') as f:
                data = f.read()
        except IOError as error:
            print('Error while reading {0:s}: {1!s}'.format(filename, error))
            exit(-1)

    results = api.match_data(data)
    if not results:
        print('No matches found.')
        exit()
    print('\n[+] Found {0:d} matches!\n'.format(len(results)))
    print('{0:<20s} {1:<55s} {2:s}'.format(
        'Name', 'ID', 'Details' if verbose else ''))
    print('{0:<20s} {1:<55s} {2:s}'.format(
        '='*10, '='*10, '='*10 if verbose else ''))
    for result in results:
        print('{0:<20s} {1:<55s} {2!s}'.format(
            result['name'],
            result['id'],
            result['details'] if verbose else ''
        ))
