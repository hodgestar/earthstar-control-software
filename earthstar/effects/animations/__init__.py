# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
from .candy_stripes import CandyStripes
from .full_pulse import FullPulse
from .lots_of_dots import LotsOfDots
from .random_worms import RandomWorms
from .ring_primary_colour import RingPrimaryColour
from .six_worm_problem import SixWormProblem
from .sparkles import Sparkles
from .three_worm_problem import ThreeWormProblem

DEFAULT_ANIMATIONS = [
    CandyStripes,
    FullPulse,
    LotsOfDots,
    RandomWorms,
    RingPrimaryColour,
    SixWormProblem,
    Sparkles,
    ThreeWormProblem,
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
