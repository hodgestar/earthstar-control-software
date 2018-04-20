# -*- coding: utf-8 -*-

""" Utilities for generating ring crossings.
"""


def generate_crossings(points, n_rings):
    """ Generate a rings crossing dictionary from crossings points.

        :param list points:
            Points is a list of rings from 0 to N-1. Each list
            specifies the LED number of each point on the ring that
            is crossed by another ring.

        :return dict:
            A dictionary of (ring_1, led_1) -> (ring_2, led_2) mappings
            that specify that (ring_1, led_1) crosses to (ring_2, led_2).
            The mapping is commutative -- so if (r1, l1) -> (r2, l2) then
            (r2, l2) -> (r1, l1) too.
    """
    assert n_rings == 6, "Crossings only supported for 6 rings."
    n_ring_crossings = 10  # only valid for n_rings == 6
    r, g, b, y, c, m = range(6)  # rings named by colour, in order
    d = {}
    # sequences
    sequences = [
        [(g, 0), (c, 8), (y, 4), (b, 6), (m, 8),
         (g, 5), (c, 3), (y, 9), (b, 1), (m, 3)],  # ring 0 (red, A)
        [(r, 0), (m, 2), (y, 1), (b, 9), (c, 2),
         (r, 5), (m, 7), (y, 6), (b, 4), (c, 7)],  # ring 1 (green, B)
        [(y, 0), (r, 8), (m, 4), (c, 6), (g, 8),
         (y, 5), (r, 3), (m, 9), (c, 1), (g, 3)],  # ring 2 (blue, C)
        [(b, 0), (g, 2), (m, 1), (c, 9), (r, 2),
         (b, 5), (g, 7), (m, 6), (c, 4), (r, 7)],  # ring 3 (yellow, D)
        [(m, 0), (b, 8), (g, 4), (r, 6), (y, 8),
         (m, 5), (b, 3), (g, 9), (r, 1), (y, 3)],  # ring 4 (cyan, E)
        [(c, 0), (y, 2), (g, 1), (r, 9), (b, 2),
         (c, 5), (y, 7), (g, 6), (r, 4), (b, 7)],  # ring 5 (magenta, F)
    ]
    # check sequencing inverses are correct
    for i, crossings in enumerate(sequences):
        for p_i, other in enumerate(crossings):
            j, p_j = other
            assert sequences[j][p_j] == (i, p_i), (
                "({}, {}) =!= ({}, {})".format(i, p_i, j, p_j))
    # check all crossings present
    points_used = [[None] * n_ring_crossings for _ in range(n_rings)]
    for i, crossings in enumerate(sequences):
        for p_i, other in enumerate(crossings):
            j, p_j = other
            points_used[j][p_j] = p_j
    expected_points_used = [
        list(range(n_ring_crossings)) for _ in range(n_rings)
    ]
    assert points_used == expected_points_used, (
        "Expected all crossings to be used")
    # crossing points
    for i, crossings in enumerate(sequences):
        for p_i, other in enumerate(crossings):
            j, p_j = other
            d[(i, points[i][p_i])] = (j, points[j][p_j])
    return d


def generate_base_crossing_points(c, n_rings):
    """ Generate a list of crossing points for each ring.

        :param int c:
            The number of LEDs in a ring.

        :return list:
            Return points as a list of rings from 0 to N-1. Each list
            specifies the LED number of each point on the ring that
            is crossed by another ring.
    """
    assert n_rings == 6, "Crossings only supported for 6 rings."
    c2 = c / 2  # mid point
    ss = c / 12  # short side
    sl = ss + (c / 32)  # long side
    ssl = ss + sl  # both sides together
    ring = [
        0, ss, ssl, c2 - ssl, c2 - ss,
        c2, c2 + ss, c2 + ssl, c - ssl, c - ss,
    ]
    crossing_points = [ring[:] for _ in range(n_rings)]
    return crossing_points
