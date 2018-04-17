# -*- coding: utf-8 -*-

""" Simple intensity adjustment for primary colours of all of the rings to produce pulses.
"""

import copy
import math

import numpy as np

from ..engine import Animation


class GradientPattern(Animation):

    ANIMATION = __name__
    ARGS = {
    }

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
        self.step = 0
        self.width = 50.0
        self.max_intensity = 255.0
        self.max_point = 40.0

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        for ring in range(self.fc.n_rings):
            intensity = [0.0] * self.fc.leds_per_ring
            gradient_up = self.max_intensity / self.max_point
            gradient_down = -1 * (self.max_intensity / (self.width - self.max_point))
            for i in range(self.fc.leds_per_ring):
                gradient = gradient_up if (i % self.width) < self.max_point else gradient_down
                intensity[i] = intensity[i - 1] + gradient
            self._rings[ring] = [i * self.fc.colour(1, 0, 0) for i in intensity]
            # self._rings[i] = np.roll(self._rings[i], 4, axis=0)
        print(gradient_up, gradient_down)
        print([int(i) for i in intensity])
        frame[:] = self._rings
