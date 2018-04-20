# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Earthstar.
"""

import numpy as np

from .crossings import generate_crossings, generate_base_crossing_points

# Fundamental constants of the ring universe
N_RINGS = 6
LEDS_PER_RING = 450
FRAME_SHAPE = (N_RINGS, LEDS_PER_RING, 4)
RING_SHAPE = (LEDS_PER_RING, 4)
FRAME_DTYPE = np.uint8

# Derived numbers of LEDs for a given fraction of a circle
C = LEDS_PER_RING
C2 = LEDS_PER_RING / 2
C4 = LEDS_PER_RING / 4
C6 = LEDS_PER_RING / 6
C8 = LEDS_PER_RING / 8

# Simulator crossings points
SIMULATOR_CROSSING_POINTS = generate_base_crossing_points(C, N_RINGS)
SIMULATOR_CROSSINGS = generate_crossings(SIMULATOR_CROSSING_POINTS, N_RINGS)

# Simulator virtual to physical mappings
SIMULATOR_VIRTUAL_TO_PHYSICAL = [
    (0, C4, False),  # virtual ring, offset in LEDs, flip (True or False)
    (1, -C4, False),
    (2, C4, False),
    (3, -C4, False),
    (4, C4, False),
    (5, -C4, False),
]

# Real earthstar crossings points
ES_CROSSING_POINTS = generate_base_crossing_points(C, N_RINGS)
ES_CROSSINGS = generate_crossings(ES_CROSSING_POINTS, N_RINGS)

# Real earthstar virtual to physical mappings
ES_VIRTUAL_TO_PHYSICAL = [
    (0, C4, False),  # virtual ring, offset in LEDs, flip (True or False)
    (1, -C4, False),
    (2, C4, False),
    (3, -C4, False),
    (4, C4, False),
    (5, -C4, False),
]


class FrameConstants(object):
    """ Holder for frame constants.

        :param int fps:
            Frames per second.
        :param str etype:
            Either "simulator" if drawing to the simulator or
            "earthstar" if drawing to the real earthstar.
    """

    def __init__(self, fps=10, etype="simulator"):
        self.n_rings = N_RINGS
        self.leds_per_ring = LEDS_PER_RING
        self.frame_shape = FRAME_SHAPE
        self.ring_shape = RING_SHAPE
        self.frame_dtype = FRAME_DTYPE
        self.c = C
        self.c2 = C2
        self.c4 = C4
        self.c8 = C8
        self.fps = fps
        if etype == "simulator":
            self.crossing_points = SIMULATOR_CROSSING_POINTS[:]
            self.crossings = SIMULATOR_CROSSINGS.copy()
            self._virtual_to_physical = SIMULATOR_VIRTUAL_TO_PHYSICAL[:]
        elif etype == "earthstar":
            self.crossing_points = ES_CROSSING_POINTS[:]
            self.crossings = ES_CROSSINGS.copy()
            self._virtual_to_physical = ES_VIRTUAL_TO_PHYSICAL[:]
        else:
            assert etype in ("simulator", "earthstar"), (
                "etype must be one of 'simulator' or 'earthstar'")

    def colour(self, r, g, b, w=0):
        """ Return a colour numpy array. """
        return np.array((b, g, r, w), dtype=self.frame_dtype)

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
                phys_frame[phys_ring] = np.flip(phys_frame[phys_ring], axis=0)
        return phys_frame
