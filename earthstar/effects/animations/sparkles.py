# -*- coding: utf-8 -*-

""" Background sparkle animation. """

import numpy as np

from ..argtypes import FloatArg, IntArg
from ..engine import Animation
from ..units.sparkle import Sparkle


class Sparkles(Animation):

    ANIMATION = __name__
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

    def post_init(self):
        self.sparkles = []
        for _ in range(5):
            self.sparkles.append(Sparkle())

    def render(self, frame):
        for sp in self.sparkles:
            sp.step()
            sp.render(frame)
