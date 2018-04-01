# -*- coding: utf-8 -*-

""" A worm that crosses rings.
"""


class Worm(object):
    def __init__(self, fc, ring, pos, speed, length, colour):
        self.fc = fc
        self.ring = ring
        self.pos = pos
        self.speed = speed
        self.length = length
        self.colour = colour
        self.crossings = []

    def step(self):
        next_pos = self.pos
        next_ring = self.ring
        for _ in range(self.speed):
            # TODO: support going in the -1 direction
            next_pos += 1
            if next_pos >= self.fc.c:
                self.crossings.insert(0, (next_ring, 0, next_ring, self.fc.c))
                next_pos = 0
            elif (next_ring, next_pos) in self.fc.crossings:
                cross_ring, cross_pos = self.fc.crossings[
                    (next_ring, next_pos)]
                self.crossings.insert(0, (
                    cross_ring, cross_pos, next_ring, next_pos))
                next_ring, next_pos = cross_ring, cross_pos
        self.pos = next_pos
        self.ring = next_ring

    def render(self, frame):
        length_remaining = self.length
        ring = self.ring
        pos = self.pos
        crossing = 0
        print("----")
        while (length_remaining > 0) and (crossing < len(self.crossings)):
            cross_ring, cross_pos, next_ring, next_pos = self.crossings[
                crossing]
            if cross_pos < pos:
                start, end = cross_pos, pos
            else:
                start, end = pos, cross_pos
            n = end - start
            n = min(n, length_remaining)
            end = start + n
            print(("C", n, start, end, length_remaining))
            if n > 0:
                frame[ring][start:end] = [self.colour] * n
            ring, pos = next_ring, next_pos
            length_remaining -= n
        if length_remaining <= 0:
            del self.crossings[crossing + 1:]
        while length_remaining > 0:
            end = min(pos + length_remaining, self.fc.c)
            n = end - pos
            print(("R", pos, end, n, length_remaining))
            if n > 0:
                frame[ring][pos:end] = [self.colour] * n
            pos = 0
            length_remaining -= n
