# -*- coding: utf-8 -*-

""" Spinning dots effects. """

import numpy as np

from .argtypes import ColourArg, FloatArg, IntArg
from .engine import Effect


class SpindotsEffect(Effect):

    EFFECT = "spindots"
    ARGS = {
        "angle": FloatArg(default=0.0),
        "colour": ColourArg(),
        "dots": IntArg(default=4, min=1, max=10),
        "rotation_speed": IntArg(default=1, min=1, max=10),
        "spread": IntArg(default=5, min=1, max=15),
        "ticks": IntArg(default=500, min=1, max=1000),
    }

    def post_init(self, angle, colour, dots, rotation_speed, spread, ticks):
        roll = int(np.round(
            self.fc.leds_per_ring * (1. + (angle / np.pi))))
        self.ticks = ticks
        self.dots = np.zeros(self.fc.ring_shape, dtype=self.fc.frame_dtype)
        for start in np.linspace(
                0, self.fc.leds_per_ring, dots, endpoint=False, dtype=int):
            for i, f in enumerate(np.linspace(0., 1., spread)):
                self.dots[start + i] = colour * f
        self.dots = np.roll(self.dots, roll, axis=0)
        self.rotation_speed = rotation_speed

    def apply(self, frame):
        self.dots = np.roll(self.dots, self.rotation_speed, axis=0)
        frame[self.ring] = np.where(
            self.dots != 0, self.dots, frame[self.ring])
        self.ticks -= 1
        return self.ticks > 0
