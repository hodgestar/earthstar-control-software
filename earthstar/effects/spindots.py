# -*- coding: utf-8 -*-

""" Spinning dots effects. """

import numpy as np

from .engine import Effect


class SpindotsEffect(Effect):

    EFFECT = "spindots"

    def post_init(self, **kw):
        self.ring = kw.get("ring")
        self.pos = int(np.round(
            self.fc.leds_per_ring * (1. + (kw["angle"] / np.pi))))
        self.pos = np.clip(self.pos, 5, self.fc.leds_per_ring - 1)
        self.ticks = 100

    def apply(self, frame):
        for i in range(5):
            frame[self.ring, self.pos - i, :] = [255, 215, 0]
        self.pos += 1
        if self.pos >= self.fc.leds_per_ring:
            self.pos = 5
        # frame[self.ring] = np.roll(frame[self.ring], 1, axis=1)
        self.ticks -= 1
        return self.ticks > 0
