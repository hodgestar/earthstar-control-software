# -*- coding: utf-8 -*-

""" Background sparkle animation. """

import random

from ..argtypes import FloatArg, IntArg
from ..engine import Animation
from ..units.sparkle import Sparkle


class Sparkles(Animation):

    ANIMATION = __name__
    ARGS = {
        # number of sparkles that appear at the start
        "n_appear": IntArg(default=50, min=1, max=30),
        # maximum number of sparkles
        "n_max": IntArg(default=150, min=1, max=200),
        # probability of sparkles being replaced if n < n_max
        "p_appear": FloatArg(default=0.05, min=0.0, max=1.0),
    }

    def post_init(self):
        self.sparkle_colours = [
            self.fc.colour(255, 255, 255),
            self.fc.colour(255, 0, 255),
            self.fc.colour(0, 0, 255),
            self.fc.colour(255, 0, 0),
        ]
        self.sparkles = []
        colour = random.choice(self.sparkle_colours)
        for _ in range(self.n_appear):
            self.sparkles.append(self.random_sparkle(colour))

    def random_sparkle(self, colour):
        ring = random.randrange(0, self.fc.n_rings)
        pos = random.randrange(0, self.fc.leds_per_ring)
        spread = random.randrange(2, 5)
        colour = random.choice(self.sparkle_colours)
        fade = random.randrange(10, 50)
        return Sparkle(self.fc, ring, pos, spread, colour, fade)

    def render(self, frame):
        for sp in self.sparkles[:]:
            sp.step()
            sp.render(frame)
            if sp.done():
                self.sparkles.remove(sp)
        if len(self.sparkles) < self.n_max:
            if random.uniform(0, 1) < self.p_appear:
                n_new = random.randint(0, self.n_max - len(self.sparkles))
                colour = random.choice(self.sparkle_colours)
                for _ in range(n_new):
                    self.sparkles.append(self.random_sparkle(colour))
