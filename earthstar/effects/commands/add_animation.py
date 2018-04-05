# -*- coding: utf-8 -*-

""" Command that adds an animation. """

from ..argtypes import DictArg, StrArg
from ..engine import Command


class AddAnimation(Command):

    COMMAND = "add-animation"
    ARGS = {
        "layer": StrArg(allow_null=True),
        "animation": DictArg(),
    }

    def apply(self, engine):
        args = self.animation.copy()
        animation_type = args.pop("type")
        engine.add_animation(animation_type, self.layer, **args)
