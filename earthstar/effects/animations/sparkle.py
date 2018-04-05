# -*- coding: utf-8 -*-

""" Background sparkle animation. """

import numpy as np

from ..argtypes import FloatArg, IntArg
from ..engine import Animation


class Sparkle(Animation):

    ANIMATION = "sparkle"
    ARGS = {
        # number of sparkles that might appear
        "n_appear": IntArg(default=5, min=1, max=20),
        # probability of each sparkle appearance
        "p_appear": FloatArg(default=0.5, min=0.1, max=1.0),
        # expect number of sparkles at equilibrium
        "n_stable": IntArg(default=100, min=1, max=100),
        # maximum number of sparkles
        "n_max": IntArg(default=150, min=1, max=200),
        # fade in / out duration
        "t_fade": IntArg(default=50, min=1, max=100),
        # spread of sparkle in leds
        "spread": IntArg(default=5, min=1, max=15),
    }

    def post_init(self, n_appear, p_appear, n_stable, n_max, t_fade, spread):
        self.n_appear = n_appear
        self.p_appear = p_appear
        self.p_die = (n_appear * p_appear) / n_stable
        self.n_max = n_max
        self.t_fade = t_fade
        self.spread = spread
        self.sparkles = []
        # roll = int(np.round(
        #     self.fc.leds_per_ring * (1. + (angle / np.pi))))
        # self.ticks = ticks
        # self.dots = np.zeros(self.fc.ring_shape, dtype=self.fc.frame_dtype)
        # for start in np.linspace(
        #         0, self.fc.leds_per_ring, dots, endpoint=False, dtype=int):
        #     for i, f in enumerate(np.linspace(0., 1., spread)):
        #         self.dots[start + i] = colour * f
        # self.dots = np.roll(self.dots, roll, axis=0)
        # self.rotation_speed = rotation_speed

    def render(self, frame):
        self.dots = np.roll(self.dots, self.rotation_speed, axis=0)
        frame[self.ring] = np.where(
            self.dots != 0, self.dots, frame[self.ring])
