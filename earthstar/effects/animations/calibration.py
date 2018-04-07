# -*- coding: utf-8 -*-

""" Calibration animation.

    Displays points at ring intersections.
"""

from ..engine import Animation


class Calibration(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    COLOURS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 100, 100),
        (100, 255, 100),
        (100, 100, 255),
    ]

    def post_init(self):
        self._white = self.fc.colour(255, 255, 255)
        self._colours = [self.fc.colour(*c) for c in self.COLOURS]
        self._crossings = {r: [] for r in range(self.fc.n_rings)}
        for src, dst in self.fc.crossings.items():
            self._crossings[src[0]].append((src, dst))
        self._tick = 0
        self._ring = 0

    def render(self, frame):
        self._tick += 1
        if self._tick >= 20:
            self._tick = 0
            self._ring = (self._ring + 1) % self.fc.n_rings
        colour = self._colours[self._ring]
        for src, dst in self._crossings[self._ring]:
            src_ring, src_pos = src
            dst_ring, dst_pos = dst
            for pos in range(src_pos, src_pos + 5):
                pos = pos % self.fc.leds_per_ring
                frame[(src_ring, pos)] = colour
            for pos in range(dst_pos, dst_pos + 5):
                pos = pos % self.fc.leds_per_ring
                frame[(dst_ring, pos)] = colour
            for pos in range(dst_pos + 5, dst_pos + 10):
                pos = pos % self.fc.leds_per_ring
                frame[(dst_ring, pos)] = self._white
