# -*- coding: utf-8 -*-

""" Sinusoidal spinning rings.
"""

import math

import numpy as np

from ..engine import Animation


class Spinners(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render_1(self):
        self.ring_len = int(float(self.fc.leds_per_ring) *
                      abs(math.sin(math.pi * (float(self.ring_pos) / (self.fc.leds_per_ring / 2)))))
        ring_off = self.fc.leds_per_ring - self.ring_len

        return ([self.colour_1] * self.ring_len) + ([self.colour_2] * ring_off)

    def ring_render_2(self):
        self.ring_len = int(float(self.fc.leds_per_ring / 2) *
                      abs(math.sin(math.pi * (float(self.ring_pos) / (self.fc.leds_per_ring / 2)))))
        ring_off = self.fc.leds_per_ring - self.ring_len

        return ([self.colour_1] * self.ring_len) + ([self.colour_2] * ring_off)

    def post_init(self):
        self.ring_pos = 0
        self.ring_len = 0
        self.colour_1 = self.fc.colour(200, 200, 200)
        self.colour_2 = self.fc.colour(0, 0, 0)

    def render(self, frame):
        return self.animation_1(frame)

    def animation_1(self, frame):
        """ A slowly spinning point that has a white bar that alternately fills the black space infront of it or behind
        it according to a sinusoidal function
        :param frame:
        :return:
        """
        self._rings = np.array([
            self.ring_render_1(),
            self.ring_render_1(),
            self.ring_render_1(),
            self.ring_render_1(),
            self.ring_render_1(),
            self.ring_render_1(),
        ], dtype=np.uint8)

        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], int(-1 * (self.ring_pos / 2)), axis=0)
        frame[:] = self._rings
        self.ring_pos = (self.ring_pos + 2) % (self.fc.leds_per_ring * 2)

    def animation_2(self, frame):
        """ Classic loader spinner
        :param frame:
        :return:
        """
        self._rings = np.array([
            self.ring_render_2(),
            self.ring_render_2(),
            self.ring_render_2(),
            self.ring_render_2(),
            self.ring_render_2(),
            self.ring_render_2(),
        ], dtype=np.uint8)

        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], self.ring_pos, axis=0)
        frame[:] = self._rings
        self.ring_pos = (self.ring_pos + 5) % (self.fc.leds_per_ring * 2)
