# -*- coding: utf-8 -*-

""" Simple intensity adjustment for primary colours of all of the rings to produce pulses.
"""

import copy
import math

import numpy as np

from ..engine import Animation


class GradientPattern(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render(self, colour_1):
        return [colour_1] * self.fc.leds_per_ring

    def post_init(self):
        self._rings = np.array([
            self.ring_render(self.fc.colour(1, 0, 0)),
            self.ring_render(self.fc.colour(0, 1, 0)),
            self.ring_render(self.fc.colour(0, 0, 1)),
            self.ring_render(self.fc.colour(1, 1, 0)),
            self.ring_render(self.fc.colour(0, 1, 1)),
            self.ring_render(self.fc.colour(1, 0, 1)),
        ], dtype=np.uint8)
        self.intensity_up = range(0, 255, 255 / self.fc.fps)
        self.intensity_down = range(250, -1, -(255 / self.fc.fps))
        self.off = [0] * len(self.intensity_up)
        self.ring_intensity = [
            self.intensity_up + self.intensity_down + self.off + self.off + self.off + self.off,
            self.off + self.intensity_up + self.intensity_down + self.off + self.off + self.off,
            self.off + self.off + self.intensity_up + self.intensity_down + self.off + self.off,
            self.off + self.off + self.off + self.intensity_up + self.intensity_down + self.off,
            self.off + self.off + self.off + self.off + self.intensity_up + self.intensity_down,
            self.intensity_down + self.off + self.off + self.off + self.off + self.intensity_up,
        ]
        self.step = 0

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        rings = copy.deepcopy(self._rings)
        for i in range(self.fc.n_rings):
            rings[i] = rings[i] * self.ring_intensity[i][self.step]
        self.step = (self.step + 1) % len(self.ring_intensity[0])
        frame[:] = rings
