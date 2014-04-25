# -*- coding: utf-8 -*-

"""
Kullback-Leibler divergence

"""

import numpy as np


def KL_divergence(p,q, domain=[-1000.0, 1000.0], step=0.1):

    """
    Compute Riemann Integral approximation
    """

    res = 0.0
    
    for i in xrange(domain[0], domain[1], step):
        res -= p(i)*np.log2(p(i)/q(i))
        
    return res
