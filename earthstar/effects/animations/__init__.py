# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
# from .calibration import Calibration  # for calibration
from .candy_stripes import CandyStripes
from .full_pulse import FullPulse
from .gradient_pattern_3 import GradientPattern as GradientPattern3
from .gradient_pattern_4 import GradientPattern as GradientPattern4
from .phase_spinners_1 import PhaseSpinners1
from .phase_spinners_2 import PhaseSpinners2
from .phase_spinners_3 import PhaseSpinners3
from .phase_spinners_4 import PhaseSpinners4
from .ring_primary_colour import RingPrimaryColour
from .six_worm_problem import SixWormProblem
from .spinners import Spinners
from .twelve_worm_problem import TwelveWormProblem
from .worms_craploads import CraploadsOfWorms
from .worms_goldfish import Goldfish
from .candy_primary import CandyStripes as CandyPrimary
from .comets import Comets
from .full_pulse_fast import FullPulse as FullPulseFast
from .spin_up import SpinUp
from .spin_up_rings import SpinUpRings

DEFAULT_ANIMATIONS = [
    CandyStripes,
    CandyPrimary,
    Comets,
    FullPulse,
    FullPulseFast,
    GradientPattern3,
    GradientPattern4,
    PhaseSpinners1,
    PhaseSpinners2,
    PhaseSpinners3,
    PhaseSpinners4,
    RingPrimaryColour,
    SixWormProblem,
    Spinners,
    SpinUp,
    SpinUpRings,
    TwelveWormProblem,
    CraploadsOfWorms,
    Goldfish,
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
