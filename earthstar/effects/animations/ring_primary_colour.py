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
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 100, 0),
        (0, 255, 100),
        (100, 0, 255),
    ]

    def post_init(self):
        self._colours = [self.fc.colour(*c) for c in self.COLOURS]
        self._tick = 0
        self.swap = 0

    def render(self, frame):
        self._ring = self.fc.empty_ring()
        self._tick += 1
        if self._tick % 10 == 0:
            self.swap = (self.swap + 1) % self.fc.n_rings
        for i in range(self.fc.n_rings):
            colour = self._colours[(self.swap + i) % self.fc.n_rings]
            frame[i] = [colour] * self.fc.leds_per_ring
