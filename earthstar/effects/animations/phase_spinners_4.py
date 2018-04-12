# -*- coding: utf-8 -*-

""" A set of points that chase a lead point in a "sinusoidal" oscillation around the ring
"""

import copy
import math

import numpy as np

from ..engine import Animation


class PhaseSpinners2(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def ring_render(self, colour_1, colour_2):
        self.stripe_width = 10
        ring_off = self.fc.leds_per_ring - self.stripe_width
        return ([colour_1] * self.stripe_width) + ([colour_2] * ring_off)

    def post_init(self):
        self.stripe_width = 4
        self._rings = np.array([
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
            self.ring_render(self.fc.colour(200, 200, 200), self.fc.colour(0, 0, 0)),
        ], dtype=np.uint8)
        self.delay = [0, 2, 4, 6, 8, 10]
        self.point_position = [0, 0, 0, 0, 0, 0]
        self.speed_increment = 1
        self.point_speed = [0, 0, 0, 0, 0, 0]

    def render(self, frame):
        return self.animation(frame)

    def animation(self, frame):
        """ 6 rings spinning in and out of phase
        :param frame:
        :return:
        """
        print('speed: %s', self.point_speed)
        print('position: %s', self.point_position)
        for i in range(self.fc.n_rings):
            if self.delay[i] <= 0:
                if self.point_position[i] < 160:
                    self.point_speed[i] += self.speed_increment
                elif self.point_position[i] < 280:
                    pass
                else:
                    self.point_speed[i] -= self.speed_increment
                self.point_position[i] = self.point_position[i] + self.point_speed[i]
                if self.point_position[i] >= self.fc.leds_per_ring:
                    self.point_speed[i] = 0
                    self.point_position[i] = 0
                self._rings[i] = np.roll(self._rings[i], self.point_speed[i], axis=0)
            else:
                self.delay[i] -= 1
        rings = copy.deepcopy(self._rings)
        rings[0] = rings[1] = rings[2] = rings[3] = rings[4] = rings[5] = rings[0] | rings[1] | rings[2] | rings[3] | rings[4] | rings[5]
        frame[:] = rings
