# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame, Series

from .dataset import DataSet
from .error_model import *

"""
Test is a class to test supervised training
It summarize results predicts by models and DataSet's target

"""


class Test:

    def __init__(self, model=None, dataset=None, error_func=square_errors):

        self.model      = model
        self.dataset    = dataset
        self.variables  = self.dataset.variables
        self.targets    = self.dataset.targets
        
        self.error_func = error_func

        if self.model != None and self.dataset != None:
            self.test()


    def test(self):

        self.results = self.model.predict(self.variables)
        self.sum_error   = self.error_func(self.resuls, self.targets)

        print "Average Error : ",self.sum_error/len(self.results)
        
        
