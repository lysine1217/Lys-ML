# -*- coding: utf-8 -*-

"""
DataSet
"""

import numpy as np
from pandas import Series, DataFrame

class DataSet:

    """
    DataSet can be used as both supervised dataset and unsupervised dataset
    Basic data structure used here is Panda
    """

    def __init__(self, dataset):

        """
        Parameter description
        dataset is raw panda dataset
        targets should be set when dataset is used in supervised training by set_target
        """
        
        self.dataset   = DataFrame(dataset)
        self.variable  = self.dataset
        self.target    = None

        self.supervise = False

    def __len__(self):
        
        return len(self.dataset)
            

    def __str__(self):

        res = "DataSet: "+len(self.dataset)
        res += "variable dim: "+self.variable[1]
        if self.target != None:
            res += "target dim: "+self.target[1]

        return res

    def __getitem__(self, i):
        return self.dataset[i]


    def __setitem__(self, i, v):
        self.dataset[i] = v


    def set_target(self, dex):
        """
        set target from self.dataset
        This automaticly set variables that are not contained in target
        """
        self.target    = self.dataset[dex]
        self.variable  = self.dataset.drop(dex, 1)
        self.supervise = True

    def set_variable(self, dex):
        
        self.variable = self.dataset[dex]


        
        

        







