# -*- coding: utf-8 -*-

""" Spinning comets.
"""

import random

import numpy as np

from ..engine import Animation


def mk_dot(fc, c, steps):
    c = fc.colour(*c)
    return [c] * steps


def mk_gradient(fc, c1, c2, steps):
    return [
        fc.colour(*c) for c in zip(
            np.linspace(c1[0], c2[0], steps),
            np.linspace(c1[1], c2[1], steps),
            np.linspace(c1[2], c2[2], steps),
        )
    ]


COLOURS = [
    [(255, 255, 0), (0, 0, 100), (0, 0, 0)],
    [(255, 0, 255), (50, 50, 200), (0, 0, 0)],
    [(0, 255, 255), (0, 0, 255), (0, 0, 0)],
]


class Comets(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._speed = self.fc.leds_per_ring / (self.fc.fps * 2)
        self._rings = []
        c1, c2, c3 = random.choice(COLOURS)
        dot = mk_dot(
            self.fc, c1, steps=self.fc.leds_per_ring / 48)
        tail = mk_gradient(
            self.fc, c1, c2, steps=self.fc.leds_per_ring / 12)
        fade = mk_gradient(
            self.fc, c2, c3, steps=self.fc.leds_per_ring / 12)
        for _ in range(self.fc.n_rings):
            ring = self.fc.empty_ring()
            ring[:] = [self.fc.colour(*c3)] * self.fc.leds_per_ring
            ring[0: len(dot)] = dot
            ring[len(dot): len(dot) + len(tail)] = tail
            ring[len(dot) + len(tail): len(dot) + len(tail) + len(fade)] = fade
            offset = random.randrange(0, self.fc.leds_per_ring)
            ring = np.roll(ring, offset, axis=0)
            self._rings.append(ring)

    def render(self, frame):
        for i in range(self.fc.n_rings):
            self._rings[i] = np.roll(self._rings[i], -self._speed, axis=0)
            frame[i:] = self._rings[i]
