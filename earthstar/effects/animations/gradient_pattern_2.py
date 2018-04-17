# -*- coding: utf-8 -*-

""" Simple intensity adjustment for primary colours of all of the rings to
    produce pulses.
"""

import math

import numpy as np

from ..engine import Animation


class GradientPattern(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render(self, colour_1):
        lights = range(self.fc.leds_per_ring)
        max_brightness = 255
        return [
            int((
                (max_brightness / 2)
                * math.sin(math.pi * float(i) / (self.fc.leds_per_ring / 2))
                ) + max_brightness / 2) * colour_1
            for i in lights
        ]

    def post_init(self):
        self._rings = np.array([
            self.ring_render(self.fc.colour(1, 0, 0)),
            self.ring_render(self.fc.colour(0, 1, 0)),
            self.ring_render(self.fc.colour(0, 0, 1)),
            self.ring_render(self.fc.colour(1, 1, 0)),
            self.ring_render(self.fc.colour(0, 1, 1)),
            self.ring_render(self.fc.colour(1, 0, 1)),
        ], dtype=np.uint8)

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], 4, axis=0)
        frame[:] = self._rings
