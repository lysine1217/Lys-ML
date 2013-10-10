#!/usr/bin/python
#
#
#
#

import numpy as np

class LogisticRegression:

    # dim is the dimensions for weight
    def __init__(self, dim):
        self.dim = dim
        self.w = np.zeros(dim+1) # for bias

    def calc(self, data):

        z = np.sum(self.w * np.array(data))
        return 1.0/(1.0+np.exp(-z))


    # training dataset should be set in following format
    # dataset = [[[v1, v2, v3], t1],
    #            [[v1, v2, v3], t2],
    #            ...]

    def train(self, dataset, rate = 0.05):
        for data in dataset:
            x = data[0]+[1.0]
            t = data[1]
            r = calc(x)
            self.w -= rate*(t-r)*x
            
    
    def stochasticGradientDescent(self, dataset, rate=0.05, iterations=10000):

        error = 0.0

        for i in xrange(iterations):
            ind = np.random.randint(0, len(dataset))
            data = dataset[ind]
            x = np.array(data[0]+[1.0])
            t = data[1]
            r = self.calc(x)
            self.w -= rate*(r-t)*x
            error += np.abs(t-r)

            if(i%100==0):
                print "error: %.6f" % error
                error = 0.0



    def predict(self, dataset, binary=1, offset=0.5):
        res = []
        for data in dataset:
            x = np.array(data+[1.0])
            r = self.calc(x)
            if(binary==1):
                if(r>offset):
                    res.append(1)
                else:
                    res.append(0)
            else:
                res.append(r)

        return res
            



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


if __name__ == "__main__":
    demoLogisticRegression()

