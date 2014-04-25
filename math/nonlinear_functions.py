# -*- coding: utf-8 -*-

"""
Nonliear functions

mainly used in neural network

"""
import numpy as np

def sigmoid(x):
    return np.tanh(x)

def dsigmoid(x):
    return 1.0 - x*x
