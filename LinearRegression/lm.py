# Linear Model
# 
# usage : python ./lm.py <file> <train dim> <iterations>
#

import sys
import numpy as np

from loader import *

class LinearModel:

    def __init__(self, train_file, train_dim=1):

        self.train_file = train_file
        self.train_dim  = train_dim + 1 #intercept

        self.train_set  = SupervisedDataSet(train_file,train_dim).data
        self.res        = np.zeros(len(self.train_set[0][1]))

        self.weight     = np.random.random(self.train_dim)
        self.dweight    = np.zeros(self.train_dim)

        for i in xrange(len(self.train_set)):
            self.train_set[i][0] = np.append(self.train_set[i][0],[1.0])
        
    def gradientDescent(self, iterations=1000, rate=0.05):
        
        for i in xrange(iterations):
            error = 0.0

            for j in xrange(1000):
            
                dex = int(np.random.random()*len(self.train_set))
                pattern = self.train_set[dex][0]
                target  = self.train_set[dex][1][0]
                
                # update
                self.res = sum(pattern*self.weight)
                error    = error + (self.res - target)**2
                
                # renewal
                self.dweight = (self.res-target)*pattern
                self.weight  = self.weight - rate * self.dweight
        
            print('error %-.8f' %error)
            print self.weight





if __name__ == "__main__":

    argv = sys.argv
    if(len(argv)<=3):
        raise IOError("The number of arguments is not appropriate")

    train_file = argv[1]
    train_dim  = argv[2]

    lm = LinearModel(train_file,(int)(train_dim))
    lm.gradientDescent(int(argv[3]))

    






