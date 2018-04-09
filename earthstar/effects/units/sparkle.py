# -*- coding: utf-8 -*-

""" Dots that spin around a ring. """

import numpy as np

from ..engine import Unit


class Sparkle(Unit):

    def __init__(self, fc, ring, pos, spread, colour, fade):
        self.fc = fc
        self.ring = ring
        self._ring = self.fc.empty_ring()
        self._ring[:spread] = colour * spread
        self._ring = np.roll(self._ring, pos, axis=0)
        self._tick = 0
        self._colour_factor = np.concatenate([
            np.linspace(0.5, 1.0, fade),
            np.array([1.0] * fade * 2),
            np.linspace(1.0, 0.5, fade),
        ])

    def done(self):
        return self._tick >= len(self._colour_factor)

    def render(self, frame):
        if self._tick < len(self._colour_factor):
            f = self._colour_factor[self._tick]
            self._tick += 1
        frame[self.ring] = np.where(
            self._ring != 0, self._ring * f, frame[self.ring])
