# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Earthstar.
"""

import numpy as np

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
C16 = LEDS_PER_RING / 16
C32 = LEDS_PER_RING / 32
FTS = C8 - C32  # full triangle side
HTS = FTS / 2


# crossing generator
def generate_crossings(points):
    """ Generate a rings crossing dictionary from crossings points. """
    d = {}
    # sequences
    sequences = [
        [(1, 0), (4, 7), (3, 4), (2, 6), (5, 7),
         (1, 5), (4, None), (2, None), (3, None), (5, 3)],  # ring 0
        [(0, 0), (5, 2), None, None, None,
         (0, 5), None, None, None, (4, 6)],  # ring 1
        [(3, 0), None, None, None, None,
         (3, 5), None, None, None, None],  # ring 2
        [(2, 0), None, None, None, None,
         (2, 5), None, None, None, None],  # ring 3
        [(5, 0), None, None, None, None,
         (5, 5), None, None, None, None],  # ring 4
        [(4, 0), None, None, None, None,
         (4, 5), None, None, None, None],  # ring 5
    ]
    # crossing points
    for i, crossings in enumerate(sequences):
        for p_i, other in enumerate(crossings):
            if not isinstance(other, tuple):
                continue
            j, p_j = other
            if p_j is None:
                continue
            d[(i, points[i][p_i])] = (j, points[j][p_j])
    # add inverse crossings
    d.update((v, k) for k, v in d.items())
    return d


# Simulator crossings points
SS = C6 / 2  # short side
SL = C6 / 2 + C32  # long side
SSL = SS + SL  # short side plus long side
SIM_RING = [
    0, SS, SSL, C2 - SSL, C2 - SS,
    C2, C2 + SS, C2 + SSL, C - SSL, C - SS,
]
SIMULATOR_CROSSING_POINTS = [SIM_RING[:] for _ in range(N_RINGS)]

# Simulator crossing
SIMULATOR_CROSSINGS = generate_crossings(SIMULATOR_CROSSING_POINTS)

# Simulator virtual to physical mappings
SIMULATOR_VIRTUAL_TO_PHYSICAL = [
    (0, C4, False),  # virtual ring, offset in LEDs, flip (True or False)
    (1, -C4, False),
    (2, C4, False),
    (3, -C4, False),
    (4, C4, False),
    (5, -C4, False),
]


class FrameConstants(object):
    """ Holder for frame constants. """
    def __init__(self, fps=10):
        self.n_rings = N_RINGS
        self.leds_per_ring = LEDS_PER_RING
        self.frame_shape = FRAME_SHAPE
        self.ring_shape = RING_SHAPE
        self.frame_dtype = FRAME_DTYPE
        self.c = C
        self.c2 = C2
        self.c4 = C4
        self.c8 = C8
        self.c16 = C16
        self.fts = FTS
        self.hts = HTS
        self.crossing_points = SIMULATOR_CROSSING_POINTS[:]
        self.crossings = SIMULATOR_CROSSINGS.copy()
        self._virtual_to_physical = SIMULATOR_VIRTUAL_TO_PHYSICAL[:]
        self.fps = fps

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
