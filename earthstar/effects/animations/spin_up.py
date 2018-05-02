# -*- coding: utf-8 -*-

""" Spin up rotating rings to maximum speed and then back down again.
"""

import random

import numpy as np

from ..engine import Animation
from ...colours import SIX_PRIMARY_COLOURS


class SpinUp(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._f = f = 24
        self._w = w = self.fc.leds_per_ring / self._f
        self._ticks = 0
        self._speeds = np.concatenate((
            np.linspace(0, 1., self.fc.fps * 3),
            np.linspace(1., 0., self.fc.fps * 3),
        ))
        self._rings = []
        colour = self.fc.colour(*random.choice(SIX_PRIMARY_COLOURS))
        for _ in range(self.fc.n_rings):
            ring = self.fc.empty_ring()
            for i in range(f / 2):
                ring[i * 2 * w:(i * 2 + 1) * w] = [colour] * w
            offset = random.randrange(0, w)
            ring = np.roll(ring, offset, axis=0)
            self._rings.append(ring)

    def render(self, frame):
        speed = int(self._w * self._speeds[self._ticks])
        self._ticks += 1
        if self._ticks >= len(self._speeds):
            self._ticks = 0
        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], speed, axis=0)
            frame[i:] = self._rings[i]
