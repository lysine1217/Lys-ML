# -*- coding: utf-8 -*-

import numpy as np

def square_errors(x_val, y_val):
    res = 0.0
    for i in xrange(len(x_val)):
        res += (x_val[i]-y_val[i])**2

    return res/len(x_val)


def class_errors(x_cls, y_cls):
    res = 0.0

    for i in xrange(len(x_cls)):
        if x_cls[i] != y_cls[i]:
            res += 1

    return res/len(x_cls)
        
def hinge_errors(x_val, y_val):
    res = 0.0

    for i in xrange(len(x_val)):
        res += np.abs(x_val[i] - y_val[i])

    return res/len(x_val)


def square_error(x_val, y_val):
    return (x-val- y_val)**2

def class_error(x_cls, y_cls):
    if x_cls == y_cls:
        return 0
    else:
        return 1

def hinge_error(x_val, y_val):
    return np.abs(x_val - y_val)



    

