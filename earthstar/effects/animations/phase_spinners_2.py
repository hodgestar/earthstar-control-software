# -*- coding: utf-8 -*-

""" A set of points that spin in and out of phase with one-another.
"""

import copy

import numpy as np

from ..engine import Animation


class PhaseSpinners2(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render(self, colour_1, colour_2):
        self.ring_len = 10
        ring_off = self.fc.leds_per_ring - self.ring_len
        return ([colour_1] * self.ring_len) + ([colour_2] * ring_off)

    def post_init(self):
        self.ring_len = 0
        self._rings = np.array([
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(
                self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
        ], dtype=np.uint8)
        self.speed = [2, 3, 5, 6, 9, 10]

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], self.speed[i], axis=0)
        rings = copy.deepcopy(self._rings)
        rings[0] = rings[1] = rings[2] = rings[3] = rings[4] = rings[5] = (
            rings[0] | rings[1] | rings[2] | rings[3] | rings[4] | rings[5])
        frame[:] = rings
