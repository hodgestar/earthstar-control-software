# -*- coding: utf-8 -*-

""" Six bright worms that womble across the earthstar.
"""

from ..engine import Animation
from ..units.worm import Worm


class SixWormProblem(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        colours = [
            (255, 0, 255),
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
        ]
        self.worms = [
            Worm(self.fc, ring=r, start=0, speed=5, length=100,
                 colour=self.fc.colour(*c))
            for r, c in enumerate(colours)
        ]

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
