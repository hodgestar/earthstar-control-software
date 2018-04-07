# -*- coding: utf-8 -*-

""" Command that adds an animation. """

from ..argtypes import IntArg
from ..engine import Command


class TransitionTimer(Command):

    COMMAND = "transition-timer"
    ARGS = {
        "seconds": IntArg(default=0, min=0),
    }

    def apply(self, engine):
        engine.set_next_transition(self.seconds)
