# -*- coding: utf-8 -*-

""" Six bright worms that womble across the earthstar.
"""

from ...colours import SIX_PRIMARY_COLOURS
from ..engine import Animation
from ..units.worm import Worm


class TwelveWormProblem(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.worms = [
            Worm(self.fc, ring=r, start=0, speed=5, length=100,
                 colour=self.fc.colour(*c))
            for r, c in enumerate(SIX_PRIMARY_COLOURS)
        ]
        self.worms += [
            Worm(self.fc, ring=r, start=(self.fc.leds_per_ring / 2), speed=5, length=100,
                 colour=self.fc.colour(*c))
            for r, c in enumerate(SIX_PRIMARY_COLOURS)
        ]

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
