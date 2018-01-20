# -*- coding: utf-8 -*-

""" HTTP API for triggering Earthstar events and
    a simple web based controller that connects to the API.

    Events are published to a ZeroMQ socket where they
    are consumed by the EffectBox (and potentially other subscribers such
    as an event logger).
"""

import click
from flask import Flask
from flask_bootstrap import Bootstrap

from .blueprints import root
from .blueprints import effect_api
from .blueprints import controller


def create_webapp():
    """Create the Earthstar web application."""
    app = Flask(__name__)
    app.register_blueprint(root.root_bp)
    app.register_blueprint(effect_api.effect_api_bp)
    app.register_blueprint(controller.controller_bp)
    Bootstrap(app)
    return app


@click.command(context_settings={"auto_envvar_prefix": "ESC"})
@click.option(
    '--host', default='localhost',
    help='IP address to listen on.')
@click.option(
    '--port', default=8080,
    help='Port to listen on.')
@click.option(
    '--debug/--no-debug', default=False,
    help='Run with debug on or off.')
def main(host, port, debug):
    """ Run the Earthstar effect API and web interface. """
    app = create_webapp()
    app.run(host=host, port=port, debug=debug)
