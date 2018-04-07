# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Earthstar.
"""

import numpy as np

# Fundamental constants of the ring universe
N_RINGS = 6
LEDS_PER_RING = 450
FRAME_SHAPE = (N_RINGS, LEDS_PER_RING, 3)
RING_SHAPE = (LEDS_PER_RING, 3)
FRAME_DTYPE = np.uint8

# Derived numbers of LEDs for a given fraction of a circle
C = LEDS_PER_RING
C2 = LEDS_PER_RING / 2
C4 = LEDS_PER_RING / 4
C8 = FTS = LEDS_PER_RING / 8  # full triangle side
C16 = HTS = LEDS_PER_RING / 16  # half triange side


class FrameConstants(object):
    """ Holder for frame constants. """
    n_rings = N_RINGS
    leds_per_ring = LEDS_PER_RING
    frame_shape = FRAME_SHAPE
    ring_shape = RING_SHAPE
    frame_dtype = FRAME_DTYPE
    c = C
    c2 = C2
    c4 = C4
    c8 = fts = C8
    c16 = hts = C16
    crossings = {
        (3, HTS): (4, -HTS % C),  # ground triangle
        (4, HTS): (5, -HTS % C),
        (5, HTS): (3, -HTS % C),
        (3, C2 + HTS): (4, C2 - HTS),  # sky triangle
        (4, C2 + HTS): (5, C2 - HTS),
        (5, C2 + HTS): (3, C2 - HTS),
    }

    def empty_ring(self):
        """ Return an numpy array for ring. """

    def empty_frame(self):
        """ Return an numpy array for frame. """
        np.zeros(
            self._frame_constants.frame_shape,
            dtype=self._frame_constants.frame_dtype)


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
