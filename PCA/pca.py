#!/bin/python2.7
# -*- coding: utf-8 -*-
#
# Principal Component Analysis
#
#



import numpy as np

class PCA:

    def __init__(self):

        self.data = None

    def predict(self, data):

        self.data  = np.array(data)

        # mean vector
        self.m     = np.mean(self.data,  axis=0)

        # variance covariance matrix for data
        self.s     = np.cov(self.data.T)

        # compute eigen value and vector
        self.v,self.w        = np.linalg.eig(self.s)

        # compute conversed vector
        self.v = self.v
        self.r = np.dot(self.data - self.m, self.w)
        
        return self.r

    def demo():
        
        data = [[1267,32],[137,137],[952,824],
                [1662,1278],[139,111],[601,304],
                [1412,1649],[629,135]]


        return self.predict(data)
        
