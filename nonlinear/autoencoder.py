# Stacked Denoising Autoencoder
# 
#
#
#

import numpy as np
import string
import sys
from neuralnetwork import *

class Layer:

    def __init__(self, ni, nh):

        self.nn = NeuralNetwork(ni, nh, ni)

    def train(self, unsupDataLst, trainingMethod=1,rate=0.0001):
        
        trainDataLst = zip(unsupDataLst, unsupDataLst)
        
        if(trainingMethod==1):
            nn.train(trainDataLst)
        else:
            nn.stochasticGradientDescent(trainDataLst)

        self.weight = self.nn.wi

    def calc(self, unsupDataLst):
        
        ret = []

        for unsupData in unsupDataLst:
            
            inputs = np.append(unsupData,[1.0])
            outputs = np.dot(inputs, self.weight)
            
            ret.append(outputs)

        return ret



class UnsupervisedAutoEncoder:


    # This class can handle multiple hidden layer
    #
    #
    
    def __init__(self, layerNum, neroNumLst):

        self.layerNum   = layerNum
        self.neroNumLst = neroNumLst
        self.layerLst = []

        self.unsupDataLst = []
        

        # check format of neroNumLst
        if(len(neroNumLst)!=layerNum+1):
            raise ValueError("The Length of neroNumLst is incorrect!")

        
        for i in xrange(self.layerNum):

            # create new layer for autoencoder            
            nLayer = Layer(neroNumLst[i],neroNumLst[i+1])
            self.layerLst.append(nLayer)
            

    def train(self, unsupDataLst):

        self.unsupDataLst = unsupDataLst
        
        # train each layer
        
        for i in xrange(self.layerNum):
            self.layerLst[i].train(self.unsupDataLst)
            self.unsupDataLst = self.layerLst[i].calc(self.unsupDataLst)


    def calc(self, unsupDataLst):

        self.unsupDataLst = unsupDataLst

        for i in xrange(self.layerNum):
            self.unsupDataLst = self.layerLst[i].calc(self.unsupDataLst)
            

        return self.unsupDataLst




class supervisedAutoEncoder:

    def __init__(self, ni, nl, nh, no):
        
        self.ni = ni  
        self.nl = nl  # number of layers
        self.nh = nh  # number of nerons in hidden layer
        self.no = no  


        self.neroNumLst = []
        
        for i in xrange(nl):
            self.neroNumLst.append((ni,ni))

        
        self.prep = unsupervisedAutoEncoder(nh,self.neroNumLst)
        
        self.supNeuralNetwork = NeuralNetwork(ni, nh, no)


    def pretrain(self, unsupDataLst):
        
        self.prep.train(unsupDataLst)


    def train(self, supDataLst):

        preTrainedDataLst = []
        
        for supData in supDataLst:
            
            inputs  = supData[0]
            outputs = supData[1]

            preTrainedInputs = self.prep.calc(inputs)
            preTrainedDataLst.append([prerTrainedInputs,outputs])

            self.supNeuralNetwork.train(preTrainedDataLst)


    def calc(self, testDataLst):

        preTrainedDataLst = []

        for testData in testDataLst:
            
            preTrainedInputs = self.prep.calc(testData)
            preTrainedDataLst.append(preTrainedInputs)

        self.supNeuralNetwork.calc(preTrainedDataLst)

        
        

        
