# -*- coding: utf-8 -*-

""" Plain ring colour animation.
    Solid colour for testing
"""

import random

from ...colours import SIX_PRIMARY_COLOURS, MANY__COLOURS
from ..engine import Animation


class RingPrimaryColour(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._colours = [c for c in SIX_PRIMARY_COLOURS]
        self._tick = 0
        self.swap = 0

    def render(self, frame):
        self._ring = self.fc.empty_ring()
        self._tick += 1
        if self._tick % self.fc.fps == 0:
            del self._colours[0]
            remaining_colours = []
            for c in MANY__COLOURS:
                if c not in self._colours:
                    remaining_colours.append(c)
            colour = random.choice(remaining_colours)
            self._colours.append(self.fc.colour(*colour))
            print(self._colours)
            self.swap = (self.swap + 1) % self.fc.n_rings
        for i in range(self.fc.n_rings):
            colour = self._colours[(self.swap + i) % self.fc.n_rings]
            frame[i] = [self.fc.colour(*colour)] * self.fc.leds_per_ring
