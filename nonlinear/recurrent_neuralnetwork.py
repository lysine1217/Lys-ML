# -*- coding: utf-8 -*-

"""
Recurrent Neural Network
"""


import numpy as np
import string
import sys

from lyspy.math.nonlinear_functions import *
from lyspy.learn.dataset import *
from lyspy.learn.test import *

class RecurrentNeuralNetwork:

    """
    Recurrent Neural Network

    """
    
    def __init__(self, ni, nh, no, tm, div=100.0, seed=False):

        # number of input, hidden and output
        self.ni = ni
        self.nh = nh
        self.no = no

        # time for backpropagation
        self.tm = tm

        # value for input
        self.vi = np.zeros(self.ni)

        # value for hidden layers
        self.vh = [np.zeros(self.nh) for i in xrange(self.tm)]  # hidden value of linear sum
        self.vz = [np.zeros(self.nh) for i in xrange(self.tm)]  # hidden value after activation

        # value for output layer
        self.vo = np.zeros(self.no)

        # set seed for reproduction
        if seed:
            np.random.seed(1)

        # weight between (input, hidden), (hidden, output), (hidden, hidden)
        self.wi = (np.random.random((self.ni,self.nh))*2.0-1.0)/div
        self.wh = (np.random.random((self.nh,self.no))*2.0-1.0)/div
        self.wp = (np.random.random((self.nh, self.nh)*2.0-1.0)/div

        # difference for wi, wh, wp
        self.di = np.zeros((self.ni,self.nh))
        self.dh = np.zeros((self.nh,self.no))
        self.dp = np.zeros((self.nh, self.nh))


        # difference for prev wi, wh, wp
        self.pdi = np.zeros((self.ni,self.nh))
        self.pdh = np.zeros((self.nh,self.no))
        self.pdp = np.zeros((self.nh, self.nh))


        # error for each layer
        self.ei = np.zeros(self.ni)
        self.eh = np.zeros(self.nh)
        self.eo = np.zeros(self.no)
        self.ep = np.zeros(self.nh)

        # square error for output
        self.so = 0.0

        # rms error list
        self.rms = []


    def update(self, inputs):
                
        # forward calculation for each layer
        self.vi = inputs
        self.vh = np.dot(self.vi,self.wi)
        self.vz = sigmoid(self.vh)
        self.vo = np.dot(self.vz,self.wh)


    def backPropagateThroughTime(self, targets, rate, momentum):
        
        """
        backporpagate the error through time

        """
        
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
        

    def test(self, dataset, detail=1):

        """
        It is recommended to do more concise test with Test module
        This is a just easy test
        """

        for i in xrange(len(dataset)):
            self.update(dataset.input[i])
            if(detail==1):
                print(dataset.input[i], '->', self.vo, 'Target :', dataset.target[i])
            else:
                print self.vo, dataset.target[i]

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


    def train(self, dataset, epoch=1000, each_epoch= 1000, rate=0.05, momentum=0.01, rate_decay=False):

        """
        Stochastic Gradient Descent training

        """

        # decrease learning rate every epoch if rate_decay is setting true
        rate_decrease = rate / epoch
        momentum_decrease = momentum / epoch

        for i in xrange(epoch):

            error = 0.0

            for j in xrange(each_epoch):

                # stochastic selection
                dex = np.random.randint(0, len(dataset))
                inputs  = dataset.input[dex]
                targets = dataset.target[dex]

                # train for new case
                self.update(inputs)
                self.backPropagate(targets, rate, momentum)

                error = error + self.so

            # calculate RMS error
            error = np.sqrt(error/each_epoch)
            self.rms.append(error)

            # update learning and momentum rate
            if rate_decay == True:
                rate -= rate_decrease
                momentum -= momentum_decrease
            
            # stop if error is small enough
            if error < 0.00001 :
                print "Converge !"
                break

            print i," epoch error %.6f" % error


    def predict(self, dataset, binary=0, threshold=0.5):

        """
        prediction using trained neural network

        binary format:
        
        1) 0: normal case
        2) 1: binarize all output with specified threshold
        3) 2: set max value to 1.0 and others to 0.0
        4) 3: set min value to 1.0 and others to 0.0

        """
        res = []
        for i in xrange(len(dataset)):
            
            # calculate for new input
            self.update(dataset.input[i])

            # case 1
            if binary==1:
                n_res = []
                for j in xrange(len(self.vo)):
                    if self.vo[j] > threshold:
                        n_res.append(1.0)
                    else:
                        n_res.append(0.0)
                res.append(n_res)

            # case 2
            elif binary==2:
                n_res = [0.0]*len(self.vo)
                max_v = np.argmax(self.vo)
                n_res[max_v] = 1.0
                res.append(n_res)

            # case 3
            elif binary==3:
                n_res = [0.0]*len(self.vo)
                min_v = np.argmin(self.vo)
                n_res[min_v] = 1.0
                res.append(n_res)

            # normal case
            else:
                res.append(self.vo)

        return np.array(res)


     
        
