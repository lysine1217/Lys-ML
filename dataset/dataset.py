# -*- coding: utf-8 -*-

"""
DataSet
"""

import numpy as np
from pandas import Series, DataFrame

class DataSet:

    """
    DataSet can be used as both supervised dataset and unsupervised dataset
    pandas.DataFrame can also be used here
    """

    def __init__(self, dataset):

        # initialize variables
        
        self.dataset   = None
        self.variables = []
        self.targets   = []

        # supervise flags
        self.supervise = False

        if isinstance(dataset, list):
            # transform list into np.array            
            self.dataset = np.array(list)

        elif isinstance(dataset, np.array):
            self.dataset = dataset

        elif isinstance(dataset, DataFrame):
            self.df      = DataFrame
            self.dataset = self.df.values.T


    def __len__(self):
        
        return len(self.dataset)
            

    def __str__(self):

        res = "DataSet: "+len(self.dataset)
        return res

    def __getitem__(self, i):
        return self.dataset[i]


    def __setitem__(self, i, v):
        self.dataset[i] = v

        
    
