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
        return [
            self.fc.colour(*c1), self.fc.colour(*c2),
        ] * (self.fc.leds_per_ring / 2)

    def post_init(self):
        self._stripes = np.array([
            self.ring_colours([0, 255, 0], [0, 0, 255]),
            self.ring_colours([128, 255, 0], [128, 0, 255]),
            self.ring_colours([255, 0, 0], [0, 0, 255]),
            self.ring_colours([255, 128, 0], [0, 128, 255]),
            self.ring_colours([255, 0, 0], [0, 255, 0]),
            self.ring_colours([255, 0, 128], [0, 255, 128]),
        ], dtype=np.uint8)

    def render(self, frame):
        frame[:] = self._stripes
