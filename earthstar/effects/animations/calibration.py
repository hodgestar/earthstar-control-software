# -*- coding: utf-8 -*-

""" Calibration animation.

    Displays points at ring intersections.
"""

from ..engine import Animation


class Calibration(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    RING_COLOURS = [
        (255, 0, 0),  # red (0)
        (0, 255, 0),  # green (1)
        (0, 0, 255),  # blue (2)
        (255, 255, 0),  # yellow (3)
        (0, 255, 255),  # turquoise (4)
        (255, 0, 255),  # purple (5)
    ]

    def post_init(self):
        ring_colours = [self.fc.colour(*c) for c in self.RING_COLOURS]
        white = self.fc.colour(255, 255, 255)
        grey = self.fc.colour(150, 150, 150)

        self._frame = self.fc.empty_frame()
        for r in range(self.fc.n_rings):
            colour = ring_colours[r]
            ring = self._frame[r]
            # crossing point markers
            for p in self.fc.crossing_points[r]:
                ring[p: p + 5] = [colour] * 5
            r_bin = "{0:03b}".format(r)
            # binary numbering
            for i in range(3):
                ring[(i * 2 + 2) * 5:(i * 2 + 3) * 5] = [
                    (white if r_bin[2 - i] == "1" else grey)] * 5

    def render(self, frame):
        frame[:] = self._frame
