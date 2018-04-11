# -*- coding: utf-8 -*-

""" Visualizing the earthstar as two sets of three rings.

    One set of three crosses in a triangle at bottom and the top (the ground
    and sky rings). The other set crosses in a triangle on the sides (the
    equatorial rings).
"""

from ..engine import Animation
from ..units.worm import Worm


class LotsOfWorms(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.worms = [
            Worm(self.fc, ring=1, start=0, speed=5, length=100,
                 colour=(0, 255, 0, 0)),
            Worm(self.fc, ring=3, start=0, speed=5, length=100,
                 colour=(0, 255, 0, 255)),
            Worm(self.fc, ring=5, start=0, speed=5, length=100,
                 colour=(0, 0, 0, 255)),
        ]

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
