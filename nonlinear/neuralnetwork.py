# -*- coding: utf-8 -*-

"""
Neural Network
"""


import numpy as np
import string
import sys

from lyspy.math.nonlinear_functions import *
from lyspy.learn.dataset import *
from lyspy.learn.test import *

class NeuralNetwork:

    """
    Neural Network
    """
    
    def __init__(self, ni, nh, no, div=100.0):

        # number of input, hidden and output
        self.ni = ni
        self.nh = nh
        self.no = no

        # value for each layer
        self.vi = np.zeros(self.ni)
        self.vh = np.zeros(self.nh) # hidden value of linear sum
        self.vz = np.zeros(self.nh) # hidden value after activation
        self.vo = np.zeros(self.no)

        # set seed for reproduction
        np.random.seed(1)

        # weight between (input, hidden) and (hidden, output)
        self.wi = (np.random.random((self.ni,self.nh))*2.0-1.0)/div
        self.wh = (np.random.random((self.nh,self.no))*2.0-1.0)/div

        # difference for wi and wh
        self.di = np.zeros((self.ni,self.nh))
        self.dh = np.zeros((self.nh,self.no))

        # difference for prev wi and wh

        self.pdi = np.zeros((self.ni,self.nh))
        self.pdh = np.zeros((self.nh,self.no))

        # error for each layer
        self.ei = np.zeros(self.ni)
        self.eh = np.zeros(self.nh)
        self.eo = np.zeros(self.no)

        # square error for output
        self.so = 0.0


    def update(self, inputs):
                
        # forward calculation for each layer
        self.vi = inputs
        self.vh = np.dot(self.vi,self.wi)
        self.vz = sigmoid(self.vh)
        self.vo = np.dot(self.vz,self.wh)


    def backPropagate(self, targets, rate, momentum):
        
        # calc errors for output layer
        self.eo = self.vo - targets
        self.so = np.sum([er*er for er in self.eo])

        # calc errors for hidden layer
        self.eh = dsigmoid(self.vz)*np.dot(self.wh,self.eo)
        
        # calc errors for weight hidden and input
        self.dh = np.dot(self.vz.reshape(self.nh,1), self.eo.reshape(1,self.no))
        self.di = np.dot(self.vi.reshape(self.ni,1), self.eh.reshape(1,self.nh))

        # update weight
        self.wh = self.wh - self.dh * rate - self.pdh * momentum
        self.wi = self.wi - self.di * rate - self.pdi * momentum

        # update dph and dpi
        self.pdh = self.dh
        self.pdi = self.di
        

        # debug
        # print "New Back"
        # print self.eo
        # print self.eh #eh is wrong ?!
        
        

        

    def test(self, patterns, resOnly=0):
        for p in patterns:
            self.update(p[0])
            if(resOnly==0):
                print(p[0], '->', self.vo, 'Target :', p[1])
            else:
                print self.vo,p[1]

    def multiclassTest(self, patterns):

        cnt1 = 0
        cnt2 = 0

        for p in patterns:
            self.update(p[0])
            res = self.vo
            ans = np.array(p[1]).argmax()
            r1  = res.argmax()
            if(ans == r1):
                cnt1+=1
                print "Correct"
            else:
                cnt2+=1
                print "Incorrect"

        print cnt1,cnt2


    def calculate(self, patterns):
        ret = []

        for p in patterns:
            self.update(p)
            print p,'->',self.vo
            ret.append(self.vo)

        return ret


    def weights(self):
        print "Input Weights"
        print wi
        print "Hidden Weights"
        print wh

    def train(self, dataset, epoch=1000, rate=0.05, momentum=0.01):

        for i in xrange(epoch):

            error = 0.0

            for j in xrange(1000):
                dex = np.random.randint(0, len(dataset))
                inputs  = dataset.input[dex]
                targets = dataset.target[dex]
                self.update(inputs)
                self.backPropagate(targets, rate, momentum)
                error = error + self.so

            if error < 0.00001 :
                print "Converge !"
                break

            print i," epoch error %.6f" % error

    
    def stochasticGradientDescent(self, patterns, iterations=1000, rate=0.05,momentum=0.01):
        for i in xrange(iterations):
            error = 0.0
            for p in xrange(1000):
                ndex = int(np.random.random()*len(patterns))
                npat = patterns[ndex]
                
                inputs  = npat[0]
                targets = npat[1]
                
                self.update(inputs)
                self.backPropagate(targets,rate,momentum)
                
                error = error + self.so

            if i%10 == 0:
                print('error %-.5f' %error)



    def predict(self, dataset, binary=0):

        res = []
        for i in xrange(len(dataset)):
            self.update(dataset.input[i])
            res.append(self.vo)

        return np.array(res)


def demo():

    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]
    
    # create a network with two input, two hidden, and one output nodes
    n = NeuralNetwork(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)

def main(argv):
    
    # Format for arguments
    # 
    # argv[1] : input file
    # argv[2] : hidden number 
    # argv[3] : iteration number
    # argv[4] : test file
    

    # parse file into trainData

    trainData = map(str.split,open(argv[1],"r").readlines())
    if(len(trainData)<1):
        raise ValueError("Text file is not long enough")

    # pat contains training data 
    # - pat[i][0] : input
    # - pat[i][1] : output
    pat = []
    for line in trainData:
        nline = map(float,line)
        pat.append([nline[:-1],[nline[-1]]])

    inputNum  = len(pat[0][0])
    hiddenNum = int(argv[2])
    outputNum = 1

    # iterations setting        
    iterationNum = 1000
    
    if(len(argv)>=4):
        iterationNum = int(argv[3])

    n = NeuralNetwork(inputNum,hiddenNum,outputNum)
    #n.stochasticGradientDescent(pat, iterations=iterationNum)
    n.train(pat,iterations=iterationNum)
    n.test(pat)

    if(len(argv)>=5):
        testData = map(str.split,open(argv[4],"r").readlines())
        testPat = []
        for line in testData:
            nline = map(float,line)
            testPat.append(nline)
            #testPat.append([nline[:-1],[nline[-1]]])

        n.calculate(testPat)


if __name__ == '__main__':

    argv = sys.argv
    main(argv)
    



     
        
