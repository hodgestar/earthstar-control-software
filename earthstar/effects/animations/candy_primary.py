# -*- coding: utf-8 -*-

""" Candy stripes in primary colours.
"""

import random

import numpy as np

from ...colours import SIX_PRIMARY_COLOURS
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
        self.stripe_width = 15
        c1 = random.choice(SIX_PRIMARY_COLOURS)
        c2 = (255, 255, 255)
        self._stripes = np.array([
            self.ring_colours(c1, c2),
            self.ring_colours(c1, c2),
            self.ring_colours(c1, c2),
            self.ring_colours(c1, c2),
            self.ring_colours(c1, c2),
            self.ring_colours(c1, c2),
        ], dtype=self.fc.frame_dtype)

    def render(self, frame):
        for i in range(self.fc.n_rings):
            self._stripes[i] = np.roll(self._stripes[i], 1, axis=0)
        frame[:] = self._stripes
