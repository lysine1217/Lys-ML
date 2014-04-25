# -*- coding: utf-8 -*-

"""
Uniform Sampler
"""

import numpy as np

def uniform_sampler(count=1000,domain=[0.0, 1.0]):

    """
    Sampling from uniform distribution

    """

    res = []

    for i in xrange(count):
        x = np.random.random()*(domain[1]-domain[0])+domain[0]
        res.append(x)

    return res

