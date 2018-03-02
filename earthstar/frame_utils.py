# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Earthstar.
"""

import numpy as np

N_RINGS = 6
LEDS_PER_RING = 100
FRAME_SHAPE = (N_RINGS, LEDS_PER_RING, 3)
RING_SHAPE = (LEDS_PER_RING, 3)
FRAME_DTYPE = np.uint8


class FrameConstants:
    """ Holder for frame constants. """
    n_rings = N_RINGS
    leds_per_ring = LEDS_PER_RING
    frame_shape = FRAME_SHAPE
    ring_shape = RING_SHAPE
    frame_dtype = FRAME_DTYPE


def candy_stripes():
    """ Return a candy striped frame. """
    def ring_colours(c1, c2):
        return [c1, c2] * (LEDS_PER_RING / 2)

    return np.array([
        ring_colours([0, 255, 0], [0, 0, 255]),
        ring_colours([128, 255, 0], [128, 0, 255]),
        ring_colours([255, 0, 0], [0, 0, 255]),
        ring_colours([255, 128, 0], [0, 128, 255]),
        ring_colours([255, 0, 0], [0, 255, 0]),
        ring_colours([255, 0, 128], [0, 255, 128]),
    ], dtype=np.uint8)
