#!/usr/bin/env python3
"""Main entry point for Yeti Python CLI utility."""

import click

from cli import match, yara_commands

@click.group()
def cli():
    pass

cli.add_command(yara_commands.yara_scan)
cli.add_command(yara_commands.dump_yara_rules)
cli.add_command(match.match)


if __name__ == '__main__':
    cli()
