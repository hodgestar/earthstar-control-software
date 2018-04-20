# -*- coding: utf-8 -*-

""" Three bright worms that womble across the earthstar.
"""

from ..engine import Animation
from ..units.worm import Worm


class ThreeWormProblem(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        colours = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
        ]
        self.worms = [
            Worm(self.fc, ring=1, start=0, speed=5, length=100,
                 colour=self.fc.colour(*colours[0])),
            Worm(self.fc, ring=3, start=0, speed=5, length=100,
                 colour=self.fc.colour(*colours[1])),
            Worm(self.fc, ring=5, start=0, speed=5, length=100,
                 colour=self.fc.colour(*colours[2])),
        ]

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
