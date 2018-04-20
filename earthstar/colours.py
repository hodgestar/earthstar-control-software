# -*- coding: utf-8 -*-

""" Colour utilties.
"""

import random

import randomcolor

# Things supported by randomcolor.RandomColor.generate
#
# hue = red, orange, yellow, green, blue, purple, pink and monochrome
#       or a float from 1. to 359.
# luminosity = bright, light or dark
# count = number of colours to generate
# format_ = rgb, rgbArray, hsl, hslArray and hex (default)

GOOD_HUES = [
    ["red", "orange"],
    ["red", "yellow"],
    ["blue", "yellow"],
    ["blue", "green"],
    ["blue", "purple"],
    ["red", "green", "blue"],
    ["pink"],
]


def random_good_hues():
    """ Return a random set of good hues. """
    return random.choice(GOOD_HUES)


def random_colours(n, hues=None, seed=None, luminosity="dark"):
    """ Generate n, random colours from the set of chosen hues.

        :type n:
            int or tuploe of two ints
        :param n:
            Number of colours. If n is a tuple or list of length 2,
            a random number of colors is chosen with randint(*n),
        :type hues:
            A list of hues or None.
        :param hues:
            A list of hues to choose from. If hues is None, hues
            is selected by calling random_good_hues.
    """
    if isinstance(n, (tuple, list)) and len(n) == 2:
        n = random.randint(*n)
    if hues is None:
        hues = random_good_hues()
    rc = randomcolor.RandomColor(seed=seed)
    d, q = divmod(n, len(hues))
    colors = []
    for hue in hues:
        colors.extend(rc.generate(
            hue=hue, luminosity=luminosity, count=d, format_="rgbArray"))
    for hue in hues[:q]:
        colors.extend(rc.generate(
            hue=hue, luminosity=luminosity, count=1, format_="rgbArray"))
    return colors
