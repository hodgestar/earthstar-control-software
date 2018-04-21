# -*- coding: utf-8 -*-

""" Lots of dots animation. """

import math
import random

from ..engine import Animation
from ..units.spindots import Spindots


class LotsOfDots(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    DOT_COLOURS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 215, 0),
    ]

    def post_init(self):
        self._colours = [
            self.fc.colour(*c) for c in self.DOT_COLOURS
        ]
        self._spindotses = []
        for ring in range(self.fc.n_rings):
            self._spindotses.extend(
                self._random_spindots(ring) for _ in range(3))

    def _random_spindots(self, ring):
        dots = random.randint(5, 20)
        angle = random.uniform(0, 2 * math.pi)
        rotation_speed = random.randint(0, 5)
        spread = random.randint(15, self.fc.leds_per_ring / dots)
        colour = random.choice(self._colours)
        return Spindots(
            self.fc, ring, angle, colour, dots, rotation_speed, spread)

    def render(self, frame):
        for dot in self._spindotses:
            dot.step()
            dot.render(frame)
