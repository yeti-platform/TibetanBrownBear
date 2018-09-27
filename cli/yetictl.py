#!/usr/bin/env python3
"""Main entry point for Yeti commands."""
import click
from cli import taxii_import
from cli import webserver
from cli import vocab_import
from cli import killchain_import

@click.group()
def cli():
    pass

cli.add_command(webserver.webserver)
cli.add_command(taxii_import.taxii_import)
cli.add_command(vocab_import.vocab_import)
cli.add_command(killchain_import.killchain_import)


if __name__ == '__main__':
    cli()
