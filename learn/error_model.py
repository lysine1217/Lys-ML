# -*- coding: utf-8 -*-

import numpy as np

def square_errors(x_val, y_val):
    res = 0.0
    for i in xrange(len(x_val)):
        res += (x_val[i]-y_val[i])**2

    return res


def class_errors(x_cls, y_cls):
    res = 0.0

    for i in xrange(len(x_cls)):
        if x_cls[i] != y_cls[i]:
            res += 1

    return res
        
def hinge_errors(x_val, y_val):
    res = 0.0

    for i in xrange(len(x_val)):
        res += np.abs(x_val[i] - y_val[i])

    return res

    

