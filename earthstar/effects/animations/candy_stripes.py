# -*- coding: utf-8 -*-

""" Candy stripes animation.
"""

import numpy as np

from ..engine import Animation


class CandyStripes(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_colours(self, c1, c2):
        c1 = self.fc.colour(*c1)
        c2 = self.fc.colour(*c2)
        pair = ([c1] * self.stripe_width) + ([c2] * self.stripe_width)
        repeats = int(np.ceil(
            float(self.fc.leds_per_ring) / (self.stripe_width * 2)))
        return (pair * repeats)[:self.fc.leds_per_ring]

    def post_init(self):
        self.stripe_width = 4
        self._stripes = np.array([
            self.ring_colours([0, 255, 0], [0, 0, 255]),
            self.ring_colours([128, 255, 0], [128, 0, 255]),
            self.ring_colours([255, 0, 0], [0, 0, 255]),
            self.ring_colours([255, 128, 0], [0, 128, 255]),
            self.ring_colours([255, 0, 0], [0, 255, 0]),
            self.ring_colours([255, 0, 128], [0, 255, 128]),
        ], dtype=np.uint8)

    def render(self, frame):
        for i in range(self.fc.n_rings):
            self._stripes[i] = np.roll(self._stripes[i], 1, axis=0)
        frame[:] = self._stripes
