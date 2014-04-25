# -*- coding: utf-8 -*-

"""
Random distribution
"""

import numpy as np

def gauss_distribution(mean=0.0, dev=1.0, count=1):
    return np.random.normal(mean, dev, count)

