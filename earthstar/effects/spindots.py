# -*- coding: utf-8 -*-

""" Spinning dots effects. """

import numpy as np

from .engine import Effect


class SpindotsEffect(Effect):

    EFFECT = "spindots"

    def post_init(self, **kw):
        self.ticks = 100
        self.dots = np.zeros(self.fc.ring_shape, dtype=self.fc.frame_dtype)
        for i in range(5):
            self.dots[i] = [255, 215, 0]
        pos = int(np.round(
            self.fc.leds_per_ring * (1. + (kw["angle"] / np.pi))))
        self.dots = np.roll(self.dots, pos, axis=0)

    def apply(self, frame):
        self.dots = np.roll(self.dots, 1, axis=0)
        frame[self.ring] = np.where(
            self.dots != 0, self.dots, frame[self.ring])
        self.ticks -= 1
        return self.ticks > 0
