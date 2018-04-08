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

# Ring crossings
CROSSINGS = {
    # Ring pair crosings
    (0, C4): (1, C2 + C4),
    (0, C2 + C4): (1, C4),
    (2, C4): (3, C2 + C4),
    (2, C2 + C4): (3, C4),
    (4, C4): (5, C2 + C4),
    (4, C2 + C4): (5, C4),
    # (3, HTS): (4, -HTS % C),  # ground triangle
    # (3, C2 + HTS): (4, C2 - HTS),  # sky triangle
}
CROSSINGS.update((v, k) for k, v in CROSSINGS.items())

# Simulator virtual to physical mappings
SIMULATOR_VIRTUAL_TO_PHYSICAL = [
    (0, 0, False),  # virtual ring, offset in LEDs, flip (True or False)
    (1, 0, False),
    (2, 0, False),
    (3, 0, False),
    (4, 0, False),
    (5, 0, True),
]


class FrameConstants(object):
    """ Holder for frame constants. """
    def __init__(self):
        self.n_rings = N_RINGS
        self.leds_per_ring = LEDS_PER_RING
        self.frame_shape = FRAME_SHAPE
        self.ring_shape = RING_SHAPE
        self.frame_dtype = FRAME_DTYPE
        self.c = C
        self.c2 = C2
        self.c4 = C4
        self.c8 = self.fts = C8
        self.c16 = self.hts = C16
        self.crossings = CROSSINGS.copy()
        self._virtual_to_physical = SIMULATOR_VIRTUAL_TO_PHYSICAL[:]

    def colour(self, r, g, b):
        """ Return a colour numpy array. """
        return np.array((r, g, b), dtype=self.frame_dtype)

    def empty_ring(self):
        """ Return an numpy array for ring. """
        return np.zeros(self.ring_shape, dtype=self.frame_dtype)

    def empty_frame(self):
        """ Return an numpy array for frame. """
        return np.zeros(self.frame_shape, dtype=self.frame_dtype)

    def virtual_to_physical(self, virt_frame):
        """ Transform a virtual frame into a phyiscal one. """
        phys_frame = self.empty_frame()
        for phys_ring, (virt_ring, offset, flip) in enumerate(
                self._virtual_to_physical):
            phys_frame[phys_ring] = np.roll(
                virt_frame[virt_ring], offset, axis=0)
            if flip:
                phys_frame[phys_ring].flip(axis=0)




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
