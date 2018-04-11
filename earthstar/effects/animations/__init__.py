# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
from .candy_stripes import CandyStripes
from .lots_of_dots import LotsOfDots
from .lots_of_worms import LotsOfWorms
from .ring_primary_colour import RingPrimaryColour
from .sparkles import Sparkles

DEFAULT_ANIMATIONS = [
    CandyStripes,
    LotsOfDots,
    LotsOfWorms,
    RingPrimaryColour,
    Sparkles,
]


def import_animation(name):
    """ Import an animation class by module name. """
    fullname = "{}.{}".format(__name__, name)
    module = __import__(fullname)
    for part in fullname.split(".")[1:]:
        module = getattr(module, part)
    objs = [getattr(module, x) for x in dir(module) if not x.startswith("_")]
    objs = [x for x in objs if type(x) == type and issubclass(x, Animation)]
    objs = [x for x in objs if x is not Animation]
    return objs[0]
