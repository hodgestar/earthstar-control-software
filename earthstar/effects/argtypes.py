# -*- coding: utf-8 -*-

""" Effect argument types. """

import random

import numpy as np


class IntArg:
    def __init__(self, default, min=None, max=None):
        self._default = default
        self._min = min
        self._max = max

    def __call__(self, v):
        try:
            v = int(v)
        except Exception:
            return self._default
        if self._min is not None:
            v = max(v, self._min)
        if self._max is not None:
            v = min(v, self._max)
        return v


class FloatArg:
    def __init__(self, default, min=None, max=None):
        self._default = default
        self._min = min
        self._max = max

    def __call__(self, v):
        try:
            v = float(v)
        except Exception:
            return self._default
        if self._min is not None:
            v = max(v, self._min)
        if self._max is not None:
            v = min(v, self._max)
        return v


class ColourArg:

    DEFAULT_COLOURS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 215, 0),
    ]

    def __init__(self):
        pass

    def __call__(self, v):
        try:
            v = (int(v[0]), int(v[1]), int(v[2]))
        except Exception:
            v = random.choice(self.DEFAULT_COLOURS)
        return np.array(v)
