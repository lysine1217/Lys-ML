# -*- coding: utf-8 -*-

"""
Kernel functions for kernel methods, svm ...
"""

import numpy as np

def GaussKernel(x1,x2, dev=1.0):
    return np.exp(-dev*(x1-x2)*(x1-x2))
