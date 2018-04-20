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
    d = {}
    # sequences
    sequences = [
        [(1, 0), (4, 7), (3, 4), (2, 6), (5, 7),
         (1, 5), (4, None), (2, None), (3, None), (5, 3)],  # ring 0
        [(0, 0), (5, 2), None, None, None,
         (0, 5), None, None, None, (4, 6)],  # ring 1
        [(3, 0), None, None, None, None,
         (3, 5), None, None, None, None],  # ring 2
        [(2, 0), None, None, None, None,
         (2, 5), None, None, None, None],  # ring 3
        [(5, 0), None, None, None, None,
         (5, 5), None, None, None, None],  # ring 4
        [(4, 0), None, None, None, None,
         (4, 5), None, None, None, None],  # ring 5
    ]
    # crossing points
    for i, crossings in enumerate(sequences):
        for p_i, other in enumerate(crossings):
            if not isinstance(other, tuple):
                continue
            j, p_j = other
            if p_j is None:
                continue
            d[(i, points[i][p_i])] = (j, points[j][p_j])
    # add inverse crossings
    d.update((v, k) for k, v in d.items())
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
