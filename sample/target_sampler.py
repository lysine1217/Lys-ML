# -*- coding: utf-8 -*-

"""
Random Sampler
"""

import numpy as np

from lyspy.math.random_distribution import *

def random_sampler(seed_f, domain=[-1.0, 1.0], count=1000, noise_dev=0.01):

    """
    Sample uniform distribution from seed_f with gauss noise
    
    """
    
    res = []

    for i in xrange(count):
        x = np.random.random()*(domain[1]-domain[0])+domain[0]
        y = seed_f(x) + gauss_distribution(0.0, noise_dev)
        res.append([x,y])

    return res

