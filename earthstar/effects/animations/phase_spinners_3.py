# -*- coding: utf-8 -*-

""" A set of points that spin in and out of phase with one-another.
"""

import copy

import numpy as np

from ..engine import Animation


class PhaseSpinners3(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render(self, colour_1, colour_2):
        pair = (
            ([colour_1] * self.stripe_width_on)
            + ([colour_2] * self.stripe_width_off))
        repeats = int(np.ceil(
            float(self.fc.leds_per_ring) / (
                self.stripe_width_on + self.stripe_width_off)))
        return (pair * repeats)[:self.fc.leds_per_ring]

    def post_init(self):
        self.stripe_width_on = 6
        self.stripe_width_off = 144
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
        self.speed = [1, 2, 3, 4, 5, 6]

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
