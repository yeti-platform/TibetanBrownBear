"""Expose Yeti's restful API on Flask's development webserver."""
import click

from yeti.common.config import yeti_config

# pylint: disable=line-too-long
@click.command()
@click.option('--debug', is_flag=True, help='launch server in debug mode', default=yeti_config.webserver.debug, type=click.BOOL)
@click.option('--interface', help='interface to listen on', default=yeti_config.webserver.interface, type=click.STRING)
@click.option('--port', help='port to listen on', default=yeti_config.webserver.port, type=click.INT)
def webserver(debug, interface, port):
    from yeti import webapp
    webapp.app.debug = debug
    webapp.app.run(host=interface, port=port)
