#!/usr/bin/env python3
"""Main entry point for Yeti server commands."""
import click
from ctl import taxii_import
from ctl import webserver
from ctl import vocab_import
from ctl import killchain_import
from ctl import user_admin

@click.group()
def cli():
    pass

cli.add_command(webserver.webserver)
cli.add_command(taxii_import.taxii_import)
cli.add_command(vocab_import.vocab_import)
cli.add_command(killchain_import.killchain_import)
cli.add_command(killchain_import.mitre_tactics_import)
cli.add_command(user_admin.add_user)
cli.add_command(user_admin.reset_password)


if __name__ == '__main__':
    cli()
