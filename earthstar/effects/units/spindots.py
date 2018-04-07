# -*- coding: utf-8 -*-

""" Dots that spin around a ring. """

import numpy as np

from ..engine import Unit


class Spindots(Unit):

    def __init__(self, fc, ring, angle, colour, dots, rotation_speed, spread):
        self.fc = fc
        self.ring = ring
        self.angle = angle
        self.colour = colour
        self.dots = dots
        self.rotation_speed = rotation_speed
        self.spread = spread
        roll = int(np.round(
            self.fc.leds_per_ring * (1. + (self.angle / np.pi))))
        self._ring = self.fc.empty_ring()
        for start in np.linspace(
                0, self.fc.leds_per_ring, self.dots,
                endpoint=False, dtype=int):
            for i, f in enumerate(np.linspace(0., 1., self.spread)):
                self._ring[start + i] = self.colour * f
        self._ring = np.roll(self._ring, roll, axis=0)

    def render(self, frame):
        self._ring = np.roll(self._ring, self.rotation_speed, axis=0)
        frame[self.ring] = np.where(
            self._ring != 0, self._ring, frame[self.ring])
