# -*- coding: utf-8 -*-

""" Engine and base classes for applying effects. """

import numpy as np

from .. import frame_utils


class EffectEngine(object):
    """ Engine for applying effects. """

    LAYERS = ['background'] + []

    def __init__(self):
        self._command_types = {}
        self._animation_types = {}
        self._frame_constants = frame_utils.FrameConstants()
        self._animation_layers = [
            'background', 'default', 'foreground',
        ]
        self._animations = dict((k, []) for k in self._animation_layers)
        self._next_transition_seconds = 60

    def add_command_type(self, command_cls):
        self._command_types[command_cls.COMMAND] = command_cls

    def add_default_command_types(self):
        from .commands import DEFAULT_COMMANDS
        for command_cls in DEFAULT_COMMANDS:
            self.add_command_type(command_cls)

    def add_animation_type(self, animation_cls):
        self._animation_types[animation_cls.ANIMATION] = animation_cls

    def add_default_animation_types(self):
        from .animations import DEFAULT_ANIMATIONS
        for animation_cls in DEFAULT_ANIMATIONS:
            self.add_animation_type(animation_cls)

    def add_animation(self, name, layer=None, **kw):
        if layer is None:
            layer = "default"
        animation_cls = self._animation_types[name]
        animation = animation_cls(self._frame_constants, **kw)
        self._animations[layer].append(animation)

    def apply_command(self, kw):
        command_cls = self._command_types[kw.pop("type")]
        command = command_cls(**kw)
        command.apply(self)

    def set_transition_timer(self, seconds):
        self._next_transition_seconds = seconds

    def next_frame(self):
        frame = np.zeros(
            self._frame_constants.frame_shape,
            dtype=self._frame_constants.frame_dtype)
        for layer in self._animation_layers:
            for animation in self._animations[layer][:]:
                animation.render(frame)
                if animation.done():
                    self._animations[layer].remove(animation)
        return frame


class Command(object):
    """ Base command class. """

    COMMAND = "unknown"
    ARGS = {}

    def __init__(self, **kw):
        self._set_args(kw)
        self.post_init()

    def _set_args(self, kw):
        for name, argtype in self.ARGS.items():
            v = argtype(kw.pop(name, None))
            setattr(self, name, v)

    def post_init(self):
        """ Post initialization set up. """

    def apply(self, engine):
        """ Apply command to the engine. """


class Animation(object):
    """ Base animation class. """

    ANIMATION = "unknown"
    ARGS = {}

    def __init__(self, frame_constants, **kw):
        self.fc = frame_constants
        self._set_args(kw)
        self.post_init()

    def _set_args(self, kw):
        for name, argtype in self.ARGS.items():
            v = argtype(kw.pop(name, None))
            setattr(self, name, v)

    def post_init(self):
        """ Post initialization set up. """

    def done(self):
        """ Return True if the animation is finished. False otherwise. """
        return False

    def render(self, frame):
        """ Render the animation to the frame. """
