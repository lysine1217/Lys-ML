# -*- coding: utf-8 -*-

"""
Logistic Regression

"""

import numpy as np

from lyspy.learn.error_model import *
from lyspy.learn.dataset import DataSet


class LogisticRegression:

    # dim is the dimensions for weight
    def __init__(self, ni, no=1):

        """
        ni: input dimension
        no: output dimension
        
        wi: weight for input
        dwi: difference for input weight
        """

        self.ni = ni
        self.no = no

        self.wi = np.zeros(self.ni)
        self.dwi  = np.zeros(self.ni)


    def calculate(self, data):
        
        z = np.dot(self.wi, data)
        return 1.0/(1.0+np.exp(-z))


    # training dataset should be set in following format
    # dataset = [[[v1, v2, v3], t1],
    #            [[v1, v2, v3], t2],
    #            ...]
    #
    #     def train(self, dataset, rate = 0.05):
    #         for data in dataset:
    #             x = data[0]+[1.0]
    #             t = data[1]
    #             r = calculate(x)
    #             self.wi -= rate*(t-r)*x


    def train(self, dataset, epoch=1000, rate=0.05):
        
        """
        Params:
        dataset should be an instance of supervised DataSet
        each epoch trains 1000 random cases
        rate defines the update rate
        """

        for i in xrange(epoch):
            error = 0.0
            
            for j in xrange(1000):
                dex = np.random.randint(0, len(dataset))
                
                v = dataset.input[dex]
                t = dataset.target[dex]

                r = self.calculate(v)
                self.wi -= rate*(t-r)*v
                error += (r-v)**2
        
            print error

            
    
#     def stochasticGradientDescent(self, dataset, rate=0.05, iterations=10000):

#         error = 0.0

#         for i in xrange(iterations):
#             ind = np.random.randint(0, len(dataset))
#             data = dataset[ind]
#             x = np.array(data[0]+[1.0])
#             t = data[1]
#             r = self.calculate(x)
#             self.wi -= rate*(r-t)*x
#             error += np.abs(t-r)

#             if(i%100==0):
#                 print "error: %.6f" % error
#                 error = 0.0



    def predict(self, dataset, binary=1, offset=0.5):
        res = []
        for i in xrange(len(dataset)):
            x = dataset.input[i]
            r = self.calculate(x)
            if binary==1:
                if r > offset:
                    res.append(1)
                else:
                    res.append(0)
            else:
                res.append(r)

        return np.array(res)


def demoLogisticRegression():

    
    # following data is about efficiency of pesticide
    # the only explaining variable is the density for pesticide
    # the target variable is the death probability

    pesticide = [[[1.5],0.01],
                 [[3.0],0.04],
                 [[4.5],0.20],
                 [[6.0],0.45],
                 [[7.5],0.75],
                 [[9.0],0.95],
                 [[10.5],0.98]]

    testset = [data[0] for data in pesticide]


    np.random.shuffle(pesticide)

    # only one variable in the model
    lr = LogisticRegression(1)
    lr.stochasticGradientDescent(pesticide)
    result = lr.predict(testset,binary=0)

    print "Result:"
    print result


