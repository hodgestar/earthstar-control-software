# -*- coding: utf-8 -*-

""" Generic tests for all animations.

    These tests run against all animation classes found in
    earthstar.effects.animations.*.
"""

import pytest

ANIMATIONS = [
    "a",
    "b",
]


@pytest.mark.parametrize("animation_cls", ANIMATIONS)
def test_generates_one_hundred_frames(animation_cls):
    """ Tests that each animation can generate one hundred
        frames correctly in a reasonable amount of time.
    """
    pass
