# -*- coding: utf-8 -*-

""" Engine and base classes for applying effects. """

import random

import numpy as np

from .. import frame_utils


class EffectEngine:
    """ Engine for applying effects. """

    LAYERS = ['background'] + []

    def __init__(self):
        self._effect_types = {}
        self._frame_constants = frame_utils.FrameConstants()
        self._effect_layers = ['background'] + [
            'ring-%d' % i for i in range(self._frame_constants.n_rings)
        ]
        self._effects = dict((k, []) for k in self._effect_layers)

    def add_type(self, effect_cls):
        self._effect_types[effect_cls.EFFECT] = effect_cls

    def add_effect(self, kw):
        effect_cls = self._effect_types[kw.pop("type")]
        ring = kw.pop("ring", None)
        ring = int(ring) if ring is not None else None
        layer = "ring-%d" % ring if ring is not None else "background"
        effect = effect_cls(self._frame_constants, ring=ring, **kw)
        self._effects[layer].append(effect)

    def next_frame(self):
        frame = np.zeros(
            self._frame_constants.frame_shape,
            dtype=self._frame_constants.frame_dtype)
        for layer in self._effect_layers:
            for effect in self._effects[layer][:]:
                keep = effect.apply(frame)
                if not keep:
                    self._effects[layer].remove(effect)
        return frame


class Effect:
    """ Base effect class. """

    EFFECT = "unknown"
    ARGS = {}

    def __init__(self, frame_constants, ring, **kw):
        self.fc = frame_constants
        self.ring = ring
        self.post_init(**self._extract_args(kw))

    def _extract_args(self, kw):
        return {
            name: argtype(kw.get(name, None))
            for name, argtype in self.ARGS.items()
        }

    def post_init(self, **kw):
        pass

    def apply(self, frame):
        """ Apply effect to the frame.

            :return: bool
                If True, keep the effect running. If False, remove
                the effect.
        """
        return False


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
