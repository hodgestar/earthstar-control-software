# -*- coding: utf-8 -*-

""" EffectBox that consumes effect events and publishes frames
    for sending to the Earthstar.

    The EffectBox polls for events regularly, attempting to publish
    frames at regular intervals. Frames are timestamped so that small
    wobbles in processing times can be sorted out in a more realtime
    process (e.g. one written in C or on the Arduino) later.

    Frames have one row per ring in the Earthstar and one column per LED
    in each ring. LEDs have three colours (RGB) so there are three bytes for
    each data point.
"""

import time

import click
import zmq

from . import frame_utils


@click.command(context_settings={"auto_envvar_prefix": "ESC"})
@click.option(
    '--effectbox-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
def main(effectbox_addr):
    click.echo("Earthstar effectbox running.")
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(effectbox_addr)
    while True:
        frame = frame_utils.candy_stripes()
        socket.send(frame.tobytes())
        click.echo("Sent frame.")
        time.sleep(1)
    click.echo("Earthstar effectbox exited.")
