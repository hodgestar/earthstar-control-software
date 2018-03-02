# -*- coding: utf-8 -*-

""" Engine and base classes for applying effects. """

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

    def __init__(self, frame_constants, ring, **kw):
        self.fc = frame_constants
        self.ring = ring
        self.post_init(**kw)

    def post_init(self, **kw):
        pass

    def apply(self, frame):
        """ Apply effect to the frame.

            :return: bool
                If True, keep the effect running. If False, remove
                the effect.
        """
        return False
