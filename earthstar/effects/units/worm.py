# -*- coding: utf-8 -*-

""" A worm that crosses rings.
"""

from ..engine import Unit


class Worm(Unit):
    """ A worm on a given ring that starts at the given position.

        A worm has a length and a speed. Speed should always be positive.
        Use a negative length to have a worm head in the opposite direction.
    """
    def __init__(self, fc, ring, start, length, speed, colour):
        self.fc = fc
        self.speed = speed
        self.colour = colour
        self.segments = []  # list of (ring, start, end)
        pos = start
        while length != 0:
            end = pos - length
            end = min(max(end, 0), self.fc.c - 1)
            self.segments.append((ring, pos, end))
            length -= (pos - end)
            # if 0 < end < self.fc.c, then neither max nor min
            # was triggered and length is 0.
            if end == 0:
                pos = self.fc.c - 1
            elif end == self.fc.c - 1:
                pos = 0

    def step(self):
        for _ in range(self.speed):
            f_ring, f_start, f_end = self.segments[0]
            f_direction = (-1, 1)[f_start >= f_end]
            n_start = f_start + f_direction
            if n_start >= self.fc.c:
                self.segments.insert(0, (f_ring, 1, 0))
                self.segments[1] = (f_ring, self.fc.c - 1, f_end)
            elif n_start <= -1:
                self.segments.insert(0, (f_ring, self.fc.c - 2, self.fc.c - 1))
                self.segments[1] = (f_ring, 0, f_end)
            else:
                self.segments[0] = (f_ring, n_start, f_end)
                if (f_ring, n_start) in self.fc.crossings:
                    c_ring, c_start = self.fc.crossings[(f_ring, n_start)]
                    self.segments.insert(0, (c_ring, c_start, c_start))

            l_ring, l_start, l_end = self.segments[-1]
            l_direction = (-1, 1)[l_start >= l_end]
            n_end = l_end + l_direction
            if n_end == l_start:
                del self.segments[-1]
            else:
                self.segments[-1] = (l_ring, l_start, n_end)

    def render(self, frame):
        for ring, start, end in self.segments:
            if end < start:
                start, end = end, start
            n = end - start
            if n > 0:
                frame[ring][start:end] = [self.colour] * n
