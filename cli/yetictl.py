#!/usr/bin/env python3
"""Main entry point for Yeti commands."""
import click
from cli import taxii_import
from cli import webserver
from cli import vocab_import
from cli import killchain_import
from cli import yara_commands
from cli import match
from cli import user_admin

@click.group()
def cli():
    pass

cli.add_command(webserver.webserver)
cli.add_command(taxii_import.taxii_import)
cli.add_command(vocab_import.vocab_import)
cli.add_command(killchain_import.killchain_import)
cli.add_command(yara_commands.yara_scan)
cli.add_command(yara_commands.dump_yara_rules)
cli.add_command(match.match)
cli.add_command(user_admin.add_user)
cli.add_command(user_admin.reset_password)


if __name__ == '__main__':
    cli()
