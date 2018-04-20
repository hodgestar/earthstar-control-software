# -*- coding: utf-8 -*-

""" Full sphere pulse.
"""

import numpy as np

from ...colours import SIX_PRIMARY_COLOURS
from ..engine import Animation


class FullPulse(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.colours = [
            self.fc.colour(*c) for c in SIX_PRIMARY_COLOURS
        ]
        self.colours.extend([
            self.fc.colour(*c) for c in [
                (255, 255, 255),
            ]
        ])
        self.step = 0
        self.colour_step = self.fc.fps * 3
        self.max_step = self.colour_step * len(self.colours)

    def render(self, frame):
        self.step += 1
        self.step %= self.max_step
        colour = self.colours[self.step / self.colour_step]
        f = np.sin(
            np.pi * float(self.step % self.colour_step) / self.colour_step
        ) ** 2
        frame[:] = (colour * f).astype(self.fc.frame_dtype)
