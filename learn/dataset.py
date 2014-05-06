# -*- coding: utf-8 -*-

"""
DataSet
"""

import numpy as np
from pandas import Series, DataFrame

class DataSet:

    """
    DataSet:

    DataSet is a class to handle training data. It used DataFrame from pandas as 
    basic structure. Both supervised dataset and unsupervised dataset can use this 
    class as a container. 
    
    """

    def __init__(self, dataset, bias=False):

        """
        Parameter description
        dataset is raw panda dataset
        variable and target will both be a numpy array
        targets should be set when dataset is used in supervised training by set_target
        """
        
        self.dataset   = DataFrame(dataset)
        self.bias      = bias
        
        # add constant bias to dataset as a variables

        if self.bias == True:
            bias_array = DataFrame(np.ones(len(self.dataset)), columns=["bias"])
            self.dataset = self.dataset.join(bias_array)


        # initially all variables in dataset will be set as input variables
            
        self.variable  = self.dataset.values
        self.target    = None


        # number of variables and targets

        self.nv        = self.dataset.shape[1]
        self.nt        = 0

        # index list for variables and targets
        # all dataset will be set as variable initially

        self.vlst      = self.dataset.columns
        self.tlst      = []

        # supervise flag will set to be true when set_target is executed

        self.supervise = False

    def __len__(self):
        
        return len(self.dataset)

    def __repr__(self):
        """
        return current status of DataSet
        """
        res = ""
        
        if self.supervise:
            res += "supervised dataset\n"
        else:
            res += "unsupervised dataset\n"
        
        res += "cases: "+str(len(self.dataset))+"\n"
        res += "variable dimension: " + str(self.variable.shape[1])+" index: "+str(self.vlst)+"\n"
        if self.supervise:
            res += "target   dimension: "+str(len(self.target))+" index: "+str(self.tlst)+"\n"

        # TODO: print top 10 cases
        return res

    def __getitem__(self, i):
        """
        getitem will fetch training case with index i
        if it is a supervise dataset getitem will return  a [variable[i], target[i]]
        else it will return variabe[i]
        """
        
        if self.supervise:
            return [self.variable[i], self.target[i]]
        else:
            return self.variable[i]

    def __setitem__(self, i, v):
        self.dataset[i] = v

    def set_target(self, dex, setVar=True):
        
        """
        set target from self.dataset
        This automaticly set variables that are not contained in target
        """

        if isinstance(dex, list):
            self.tlst = dex
        else:
            self.tlst = [dex]

        if setVar == True:
            self.vlst = [x for x in self.dataset.columns if x not in self.tlst]
        
        self.target    = self.dataset[dex].values
        self.variable  = self.dataset.drop(dex, 1).values
        self.supervise = True


    def set_variable(self, dex):

        if isinstance(dex, list):
            self.vlst = dex
        else:
            self.vlst = [dex]

        self.variable = self.dataset[dex].values


    def add_variable(self, dataset):

        self.dataset.join(dataset)









        
        

        







