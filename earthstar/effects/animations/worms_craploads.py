# -*- coding: utf-8 -*-

""" Six bright worms that womble across the earthstar.
"""


import random

from ...colours import random_colours
from ..engine import Animation
from ..units.worm import Worm


class CraploadsOfWorms(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.worms = []
        for c in random_colours((100, 100)):
            c = tuple([min(255, i * 1.5) for i in c])
            ring = random.randrange(0, self.fc.n_rings)
            start = random.choice([
                0, self.fc.c4, self.fc.c2, self.fc.c2 + self.fc.c4])
            speed = random.randint(2, 5)
            length = 20
            turns = [random.randint(0, 2) - 1, random.randint(0, 2) - 1, random.randint(0, 2) - 1,
                     random.randint(0, 2) - 1, random.randint(0, 2) - 1, random.randint(0, 2) - 1,
                     random.randint(0, 2) - 1, random.randint(0, 2) - 1, random.randint(0, 2) - 1]
            self.worms.append(Worm(
                self.fc, ring=ring, start=start, speed=speed, length=length,
                colour=self.fc.colour(*c), turns=turns))

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
