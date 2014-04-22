# -*- coding: utf-8 -*-

"""
Gibbs Sampler

This program just computes specific normal distribution.
"""

import numpy as np

def gibbs_sampler(count=1000):

    res = []
    x = [0.0,0.0]
    
    res.append(x)
    r = 0.5

    for i in xrange(count):
        x1 = np.random.normal(res[i][1]*r, np.sqrt(1-r**2))
        x2 = np.random.normal(x1*r, np.sqrt(1-r**2))
        res.append([x1,x2])

    return res
            
