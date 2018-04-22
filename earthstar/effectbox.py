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
from .effects.animations import import_animation
from .frame_utils import FrameConstants


@click.command(context_settings={"auto_envvar_prefix": "ESC"})
@click.option(
    '--fps', default=17,
    help='Frames per second.')
@click.option(
    '--etype', default="earthstar",
    type=click.Choice(["earthstar", "simulator"]))
@click.option(
    '--transition', default=60,
    help='Time between animation transitions.')
@click.option(
    '--animation', default=None,
    help='Run only a selected animation.')
@click.option(
    '--effect-addr', default='tcp://127.0.0.1:5555',
    help='ZeroMQ address to receive events from.')
@click.option(
    '--frame-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
def main(fps, etype, transition, animation, effect_addr, frame_addr):
    click.echo("Earthstar effectbox running.")
    tick = 1. / fps
    context = zmq.Context()
    frame_socket = context.socket(zmq.PUB)
    frame_socket.bind(frame_addr)
    effect_socket = context.socket(zmq.SUB)
    effect_socket.connect(effect_addr)
    effect_socket.setsockopt_string(zmq.SUBSCRIBE, u"")  # receive everything

    fc = FrameConstants(fps=fps, etype=etype)
    engine = EffectEngine(fc=fc, tick=tick, transition=transition)
    engine.add_default_command_types()
    if animation:
        for name in animation.split(','):
            engine.add_animation_type(import_animation(name))
    else:
        engine.add_default_animation_types()

    while True:
        start = time.time()
        try:
            effect = effect_socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError as err:
            if not err.errno == zmq.EAGAIN:
                raise
        else:
            engine.apply_command(json.loads(effect))
        frame = engine.next_frame()
        frame = fc.virtual_to_physical(frame)
        frame_socket.send(frame.tobytes())
        sleep_time = tick - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
    click.echo("Earthstar effectbox exited.")
