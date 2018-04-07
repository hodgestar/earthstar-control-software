# -*- coding: utf-8 -*-

""" Spinning dots animation. """

import numpy as np

from ..argtypes import ColourArg, FloatArg, IntArg
from ..engine import Animation


class Spindots(Animation):

    ANIMATION = "spindots"
    ARGS = {
        "ring": IntArg(default=0, min=0),
        "angle": FloatArg(default=0.0),
        "colour": ColourArg(),
        "dots": IntArg(default=4, min=1, max=10),
        "rotation_speed": IntArg(default=1, min=1, max=10),
        "spread": IntArg(default=5, min=1, max=15),
        "ticks": IntArg(default=500, min=1, max=1000),
    }

    def post_init(self):
        roll = int(np.round(
            self.fc.leds_per_ring * (1. + (self.angle / np.pi))))
        self._ring = np.zeros(self.fc.ring_shape, dtype=self.fc.frame_dtype)
        for start in np.linspace(
                0, self.fc.leds_per_ring, self.dots,
                endpoint=False, dtype=int):
            for i, f in enumerate(np.linspace(0., 1., self.spread)):
                self._ring[start + i] = self.colour * f
        self._ring = np.roll(self._ring, roll, axis=0)

    def done(self):
        return self.ticks <= 0

    def render(self, frame):
        self._ring = np.roll(self._ring, self.rotation_speed, axis=0)
        frame[self.ring] = np.where(
            self._ring != 0, self._ring, frame[self.ring])
        self.ticks -= 1
