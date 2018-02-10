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
import zmq

from .blueprints import root
from .blueprints import effect_api
from .blueprints import controller


def create_effect_socket(effect_addr):
    """ Create effect socket. """
    context = zmq.Context()
    effect_socket = context.socket(zmq.PUB)
    effect_socket.bind(effect_addr)
    return effect_socket


def create_webapp(effect_socket):
    """ Create the Earthstar web application. """
    app = Flask(__name__)
    app.effect_socket = effect_socket
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
    '--effect-addr', default='tcp://127.0.0.1:5555',
    help='ZeroMQ address to publish events to.')
@click.option(
    '--debug/--no-debug', default=False,
    help='Run with debug on or off.')
def main(host, port, effect_addr, debug):
    """ Run the Earthstar effect API and web interface. """
    effect_socket = create_effect_socket(effect_addr)
    app = create_webapp(effect_socket)
    app.run(host=host, port=port, debug=debug)
