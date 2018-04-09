# -*- coding: utf-8 -*-

""" Plain ring colour animation.

    Solid colour for testing
"""

from ..engine import Animation


class RingPrimaryColour(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    COLOURS = [
        (0, 255, 0, 0),
        (0, 0, 255, 0),
        (0, 0, 0, 255),
        (0, 255, 100, 0),
        (0, 0, 255, 100),
        (0, 100, 0, 255),
    ]

    def post_init(self):
        self._colours = [self.fc.colour(*c) for c in self.COLOURS]
        self._tick = 0

    def render(self, frame):
        self._ring = self.fc.empty_ring()
        #self._tick += 1
        for i in range(self.fc.n_rings):
            colour = self._colours[i]
            frame[i][0:self.fc.leds_per_ring] = [colour] * self.fc.leds_per_ring
