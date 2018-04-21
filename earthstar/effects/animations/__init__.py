# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
# from .calibration import Calibration  # for calibration
from .candy_stripes import CandyStripes
from .full_pulse import FullPulse
from .gradient_pattern_1 import GradientPattern as GradientPattern1
from .gradient_pattern_2 import GradientPattern as GradientPattern2
from .gradient_pattern_3 import GradientPattern as GradientPattern3
from .gradient_pattern_4 import GradientPattern as GradientPattern4
from .lots_of_dots import LotsOfDots
from .phase_spinners_1 import PhaseSpinners as PhaseSpinners1
from .phase_spinners_2 import PhaseSpinners2
from .phase_spinners_3 import PhaseSpinners3
from .phase_spinners_4 import PhaseSpinners4
from .random_worms import RandomWorms
from .ring_primary_colour import RingPrimaryColour
from .six_worm_problem import SixWormProblem
# from .sparkles import Sparkles  # doesn't look great
from .three_worm_problem import ThreeWormProblem

DEFAULT_ANIMATIONS = [
    CandyStripes,
    FullPulse,
    GradientPattern1,
    GradientPattern2,
    GradientPattern3,
    GradientPattern4,
    LotsOfDots,
    PhaseSpinners1,
    PhaseSpinners2,
    PhaseSpinners3,
    PhaseSpinners4,
    RandomWorms,
    RingPrimaryColour,
    SixWormProblem,
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
