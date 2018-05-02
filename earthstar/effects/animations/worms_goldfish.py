# -*- coding: utf-8 -*-

""" Six bright worms that womble across the earthstar.
"""

from ..engine import Animation
from ..units.worm import Worm


class Goldfish(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def create_fishes(self, speed, length, c):
        ring = 0
        start = 5
        turns = [-1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 1) / 10) + 10
        turns = [-1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 2) / 10) + 10
        turns = [-1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 3) / 10) + 10
        turns = [1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 4) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 5) / 10) + 10
        turns = [-1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 6) / 10) + 10
        turns = [-1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 7) / 10) + 10
        turns = [-1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 8) / 10) + 10
        turns = [1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 9) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        ring = 1
        start = ((self.fc.leds_per_ring * 8) / 10) + 10
        turns = [-1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 7) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 6) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        ring = 4
        start = ((self.fc.leds_per_ring * 4) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 5) / 10) + 10
        turns = [-1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        ring = 2
        start = ((self.fc.leds_per_ring * 7) / 10) + 10
        turns = [-1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 8) / 10) + 10
        turns = [1, -1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 9) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        ring = 3
        start = ((self.fc.leds_per_ring * 1) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))
        start = ((self.fc.leds_per_ring * 2) / 10) + 10
        turns = [1, 1, 1]
        self.worms.append(Worm(
            self.fc, ring=ring, start=start, speed=speed, length=length,
            colour=self.fc.colour(*c), turns=turns))

    def post_init(self):
        self.worms = []
        self.create_fishes(2, 30, (255, 15, 0))
        self.create_fishes(1, 3, (255, 255, 255))

    def render(self, frame):
        for worm in self.worms:
            worm.step()
            worm.render(frame)
