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

import json
import time

import click
import zmq

from .effects.engine import EffectEngine


@click.command(context_settings={"auto_envvar_prefix": "ESC"})
@click.option(
    '--fps', default=10,
    help='Frames per second.')
@click.option(
    '--transition', default=60,
    help='Time between animation transitions.')
@click.option(
    '--effect-addr', default='tcp://127.0.0.1:5555',
    help='ZeroMQ address to receive events from.')
@click.option(
    '--frame-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
def main(fps, transition, effect_addr, frame_addr):
    click.echo("Earthstar effectbox running.")
    tick = 1. / fps
    context = zmq.Context()
    frame_socket = context.socket(zmq.PUB)
    frame_socket.bind(frame_addr)
    effect_socket = context.socket(zmq.SUB)
    effect_socket.connect(effect_addr)
    effect_socket.setsockopt_string(zmq.SUBSCRIBE, u"")  # receive everything

    engine = EffectEngine(tick=tick, transition=transition)
    engine.add_default_command_types()
    engine.add_default_animation_types()

    while True:
        try:
            effect = effect_socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError as err:
            if not err.errno == zmq.EAGAIN:
                raise
        else:
            engine.apply_command(json.loads(effect))
        frame = engine.next_frame()
        frame_socket.send(frame.tobytes())
        time.sleep(tick)
    click.echo("Earthstar effectbox exited.")
