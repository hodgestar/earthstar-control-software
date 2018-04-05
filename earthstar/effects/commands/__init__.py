# -*- coding: utf-8 -*-

""" Commands package. """

from .add_animation import AddAnimation
from .transition_timer import TransitionTimer

DEFAULT_COMMANDS = [
    AddAnimation,
    TransitionTimer,
]
