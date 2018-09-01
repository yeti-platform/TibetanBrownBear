#!/usr/bin/env python3
"""Main entry point for Yeti commands."""
import click
from cli import taxii_import
from cli import webserver

@click.group()
def cli():
    pass

cli.add_command(webserver.webserver)
cli.add_command(taxii_import.taxii_import)


if __name__ == '__main__':
    cli()
