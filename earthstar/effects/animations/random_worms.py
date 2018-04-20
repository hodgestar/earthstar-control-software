# -*- coding: utf-8 -*-

""" Lots of random worms that womble across the earthstar.

    I.e. earthworms. :)
"""

import random

from ...colours import random_colours
from ..engine import Animation
from ..units.worm import Worm


class RandomWorms(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.worms = []
        for c in random_colours((3, 12)):
            ring = random.randrange(0, self.fc.n_rings)
            start = random.choice([
                0, self.fc.c4, self.fc.c2, self.fc.c2 + self.fc.c4])
            speed = random.randint(3, 5)
            length = random.randint(100, 120)
            self.worms.append(Worm(
                self.fc, ring=ring, start=start, speed=speed, length=length,
                colour=self.fc.colour(*c)))

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
