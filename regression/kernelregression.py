# -*- coding: utf-8 -*-

"""
Kernel Regression
"""

import numpy as np

from lyspy.math.kernel_functions import *

class KernelRegression:

    """
    Kernel Regression
    """

    def __init__(self, kernel=GaussKernel):

        self.train_data = None
        self.test_data  = None

        self.kernel = kernel

    def train(self, train_data):

        """
        Compute W=K^-1*y

        """

        self.train_data = train_data
        self.target = []
        self.dim = len(train_data)
        self.gram_matrix = np.zeros([self.dim, self.dim])

        for i in xrange(self.dim):
            self.target.append(train_data[i][1])

        for i in xrange(self.dim):
            for j in xrange(self.dim):
                self.gram_matrix[i][j] = self.kernel(train_data[i][0], train_data[j][0])


        self.weight = np.dot(np.linalg.inv(self.gram_matrix), self.target)

        
    
    def predict(self, test_data):

        """
        Compute y = sum_j (aj * k(xj, x))

        """

        self res = []

        for i in xrange(len(test_data)):
            res_i = 0.0
            
            for j in xrange(self.dim):
                res_i += self.weight[j] * self.kernel(test_data[i], 
                                                      self.train_data[j][0])

            self.res.append(res_i)


        return res

            
        
