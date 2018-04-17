# -*- coding: utf-8 -*-

""" Simple intensity adjustment for primary colours of all of the rings to produce pulses.
"""

import math
import random

import numpy as np

from ..engine import Animation


class GradientPattern(Animation):

    ANIMATION = __name__
    ARGS = {
    }
    WIDTH = [15.0, 25.0, 30.0, 45.0, 50.0, 75.0, 150.0]

    def ring_render(self, colour_1):
        return [colour_1] * self.fc.leds_per_ring

    def post_init(self):
        self._rings = np.array([
            self.ring_render(self.fc.colour(1, 0, 0)),
            self.ring_render(self.fc.colour(0, 1, 0)),
            self.ring_render(self.fc.colour(0, 0, 1)),
            self.ring_render(self.fc.colour(1, 1, 0)),
            self.ring_render(self.fc.colour(0, 1, 1)),
            self.ring_render(self.fc.colour(1, 0, 1)),
        ], dtype=np.uint8)
        self.width = self.WIDTH[random.randint(0, len(self.WIDTH) - 1)]
        self.max_intensity = 255.0
        self.colour_combos = [
            [self.fc.colour(1, 0, 0), self.fc.colour(0, 1, 0)],
            [self.fc.colour(1, 0, 0), self.fc.colour(0, 0, 1)],
            [self.fc.colour(1, 0, 0), self.fc.colour(0, 1, 1)],
            [self.fc.colour(0, 1, 0), self.fc.colour(0, 0, 1)],
            [self.fc.colour(0, 1, 0), self.fc.colour(1, 0, 1)],
            [self.fc.colour(0, 0, 1), self.fc.colour(1, 1, 0)],
        ]
        self.cycle_speed = 100
        self.position = 0

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        for ring in range(self.fc.n_rings):
            intensity = [0.0] * self.fc.leds_per_ring
            self.max_point = int((self.width / 2) + ((self.width/2) - 1) * (math.sin(math.pi * self.position / (self.cycle_speed / 2))))
            gradient_up = self.max_intensity / self.max_point
            gradient_down = -1 * (self.max_intensity / (self.width - self.max_point))
            for i in range(self.fc.leds_per_ring):
                gradient = gradient_up if (i % self.width) < self.max_point else gradient_down
                intensity[i] = intensity[i - 1] + gradient
            self._rings[ring] = [i * self.colour_combos[ring][0] for i in intensity]
            self._rings[ring] = np.roll(self._rings[ring], int(self.width / 2), axis=0)
            self._rings[ring] = np.add(self._rings[ring], [i * self.colour_combos[ring][1] for i in intensity])

        self.position = (self.position + 1) % self.cycle_speed
        frame[:] = self._rings
