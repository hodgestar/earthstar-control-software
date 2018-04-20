# -*- coding: utf-8 -*-

""" A worm that crosses rings.
"""

from ..engine import Unit


class Worm(Unit):
    """ A worm on a given ring that starts at the given position.

        A worm has a length and a speed. Speed should always be positive.
        Use a negative length to have a worm head in the opposite direction.

        :param list turns:
            List of 1, 0, or -1 values specifying the sequence of turns
            a worm should take. 1 indicates turn onto the positive ring
            direction. -1 indicates turn onto the negative ring direction.
            0 indicates not to turn.
    """
    def __init__(self, fc, ring, start, length, speed, colour, turns=None):
        self.fc = fc
        self.speed = speed
        self.colour = colour
        self.segments = []  # list of (ring, start, end)
        self._turns = turns if turns is not None else [1, -1]
        self._turn_pos = 0
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

    def _do_turn(self, f_ring, f_start):
        direction = self._turns[self._turn_pos]
        self._turn_pos = (self._turn_pos + 1) % len(self._turns)
        c_ring, c_start = self.fc.crossings[(f_ring, f_start)]
        if direction == 1:
            self.segments.insert(0, (c_ring, c_start + 1, c_start))
        elif direction == -1:
            self.segments.insert(0, (c_ring, c_start, c_start + 1))
        else:
            pass  # don't start a new segment for places we don't turn

    def step(self):
        for _ in range(self.speed):
            f_ring, f_start, f_end = self.segments[0]
            f_direction = (-1, 1)[f_start >= f_end]
            n_start = f_start + f_direction
            if n_start >= self.fc.c:
                if (f_ring, 0) in self.fc.crossings:
                    self._do_turn(f_ring, 0)
                else:
                    self.segments.insert(0, (f_ring, 1, 0))
                self.segments[1] = (f_ring, self.fc.c - 1, f_end)
            elif n_start <= -1:
                # there can't be a crossing at n_start == self.fc.c, so no need
                # to check
                self.segments.insert(0, (f_ring, self.fc.c - 2, self.fc.c - 1))
                self.segments[1] = (f_ring, 0, f_end)
            else:
                self.segments[0] = (f_ring, n_start, f_end)
                if (f_ring, n_start) in self.fc.crossings:
                    self._do_turn(f_ring, n_start)

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
            end += 1  # draw all the way to the end of the range
            n = end - start
            if n > 0:
                frame[ring][start:end] = [self.colour] * n
