# -*- coding: utf-8 -*-

"""
Linear Regression

"""

import numpy as np

from lyspy.learn.dataset import DataSet
from lyspy.learn.test import Test


class LinearRegression:

    def __init__(self, ni, no=1):

        """
        ni: input dimension
        no: output dimension
        """

        self.ni = ni
        self.no = no

        self.wi  = np.random.random(self.ni)
        self.dwi = np.zeros(self.ni)

    def calculate(self, v):
        return np.dot(v, self.wi)

    def train(self, dataset, epoch=1000, rate=0.05):
        
        """
        dataset should be an instance of supervised DataSet
        
        """

        for i in xrange(epoch):
            error = 0.0

            for j in xrange(1000):
                dex = np.random.randint(0, len(dataset))

                v = dataset.variable[dex]
                t = dataset.target[dex]

                r = self.calculate(v)
                error += (r-t)**2
                
                self.dwi = (r-t)*v
                self.wi  = self.wi - rate*self.dwi

            print i," epoch error %.6f" % error

    def predict(self, dataset):
        
        res = []
        
        for i in xrange(len(dataset)):
            v = dataset.variable[i]
            r = self.calculate(v)
            res.append(r)

        return np.array(res)
