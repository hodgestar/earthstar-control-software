# -*- coding: utf-8 -*-

""" Visualizing the earthstar as two sets of three rings.

    One set of three crosses in a triangle at bottom and the top (the ground
    and sky rings). The other set crosses in a triangle on the sides (the
    equatorial rings).
"""

import numpy as np

from ..engine import Animation
from ..units.worm import Worm


class GroundAndSky(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.n_lit_min = 10
        self.n_lit_max = self.fc.leds_per_ring
        self.n_lit = self.n_lit_min
        self.direction = 10
        self.ring_colours = [
            (255, 150, 150),  # Equatorial
            (255, 150, 150),  # Equatorial
            (255, 150, 150),  # Equatorial
            (100, 100, 255),  # Ground and sky
            (100, 150, 255),  # Ground and sky
            (100, 200, 255),  # Ground and sky
        ]
        self.ring_offsets = [
            390, 0, 0,  # Equatorial
            225, 315, 135,  # Ground and sky
        ]
        self.sky = [3, 4, 5]
        self.tick = 0
        self.worm = Worm(
            self.fc, ring=3, pos=0, speed=5, length=100, colour=(255, 0, 255))

    def render(self, frame):
        self.worm.step()
        if ((self.direction < 0 and self.n_lit > self.n_lit_min)
                or (self.direction > 0 and self.n_lit < self.n_lit_max)):
            self.n_lit += self.direction
        else:
            self.direction = -self.direction
        for i in range(self.fc.n_rings):
            colour = self.ring_colours[i]
            offset = 0
            if i in self.sky:
                n = self.n_lit_max
                # offset = n / 2
            else:
                n = self.n_lit_max
            frame[i][0:n] = [colour] * n
            frame[i] = np.roll(frame[i], offset, axis=0)
        self.worm.render(frame)
        for i in range(self.fc.n_rings):
            frame[i] = np.roll(frame[i], self.ring_offsets[i], axis=0)
