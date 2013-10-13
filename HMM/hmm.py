#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Hidden Markov Model
#
#  Description:
#
#   Simple implementation of first order HMM. 
#   All latent and observed class should be discrete
# 
#  Dependency:
#
#   numpy
#

import numpy as np



class HMM:

    # lcls: latent class labels
    # ocls: observed class labels
    # pll : probability for latent label to latent label
    # plo : probability for latent label to observed label

    def __init__(self, lcls, ocls, pll=[], plo=[]):
        
        self.lcls = lcls
        self.ocls = ocls


        # size of latent classes and observed classex
        self.sl   = len(self.lcls)
        self.so   = len(self.ocls)
        
        # map for latent index to latent name and others
        self.mlin  = {i: v for i,v in enumerate(self.lcls)}
        self.mlni  = {v: i for i,v in enumerate(self.lcls)}

        # map for observed index to observed name
        self.moin  = {i: v for i,v in enumerate(self.ocls)}
        self.moni  = {v: i for i,v in enumerate(self.ocls)}

        # transition matrix
        if(pll!=[]):
            self.pll = np.array(pll)
        else:
            self.pll = np.zeros([self.sl, self.sl])

        if(plo!=[]):
            self.plo = np.array(plo)
        else:
            self.plo = np.zeros([self.sl, self.so])

        # count for latent labels
        self.cl = np.zeros(self.sl)


    # dataset should be set into following format
    # dataset = [ (L1, O1), (L2, O2), (L3, O3) ...]
    # Li : ith list of latent labels
    # Oi : ith list of observed lables
    # Be careful that len(Xi)==len(Yi) for every i

    def train(self, dataset, llsmoothing=0, losmoothing=0):

        # count number of L_{i} | L_{i-1} and O_{i} | L_{i} 
        for vlat, vobs in dataset:
            for i in xrange(len(vobs)-1):
                
                lat  = self.mlni[vlat[i]]
                nlat = self.mlni[vlat[i+1]]

                self.cl[lat] += 1
                self.pll[lat][nlat] += 1

                if(self.moni.has_key(vobs[i])):
                    obs  = self.moni[vobs[i]]
                    self.plo[lat][obs]  += 1

            # last pair element
            lat = self.mlni[vlat[-1]]
            self.cl[lat] += 1

            if(self.moni.has_key(vobs[-1])):
                obs = self.moni[vobs[-1]]
                self.plo[lat][obs] +=1


        # latent to latent smoothing
        for i in xrange(self.sl):
            sll = np.sum(self.pll[i])+llsmoothing*self.sl
            if(sll==0.0):
                continue

            for j in xrange(self.sl):
                self.pll[i][j] = (self.pll[i][j] + llsmoothing)/sll


        # latent to observed smoothing
        slo = self.cl + np.ones(self.sl)*losmoothing*self.so

        for i in xrange(self.sl):
            if(slo[i] == 0.0):
                continue

            for j in xrange(self.so):
                self.plo[i][j] = (self.plo[i][j] + losmoothing)/slo[i]

        
        # for debug
        # print "PLO"
        # print self.plo
        # print "PLL"
        # print self.pll
        

    
    # calculate latent label for a single observed data

    def calculate(self, obs):

        res = []
        
        # probability list
        plst = []

        # start probability for latent lables P(L0)
        pl  = self.cl/np.sum(self.cl)

        # P(O0|L0)*P(L0)
        fst = self.moni[obs[0]]
        pl  = pl * self.plo[:,fst]
        plst.append(np.copy(pl))


        # forward calculate
        for i in xrange(1,len(obs)):
            obj = self.moni[obs[i]]
            pl  = np.dot(pl, self.pll)
            pl  = pl * self.plo[:,obj]
            plst.append(np.copy(pl))
            
        # backward calculate
        mp = np.argmax(plst[-1])
        res.append(self.mlin[mp])

        for i in xrange(len(obs)-2, -1, -1):
            
            pl = self.pll[:,mp]*plst[i]
            mp = np.argmax(pl)
            res.append(self.mlin[mp])
        

        # reverse
        return res[::-1]

    # dataset should be set into following format
    # dataset = [ O1, O2, O3 ... ]
    # output will be [ L1, L2, L3 ... ]

    def predict(self, dataset):

        latlst = []
        for obs in dataset:
            lat = self.calculate(obs)
            rlst.append(lat)

        return latlst


    # testset should be the same format as trainset
    # testset = [ [L1, O1], [L2, O2], [L3, O3] ... ]
        
    def test(self, testset, printlog=1):

        cnt_correct = 0
        cnt_wrong   = 0
        
        for lat, obs in testset:
            res = self.calculate(obs)
            if(res == lat):
                cnt_correct += 1
                if(printlog==1):
                    print "Correct"
            else:
                cnt_wrong += 1
                if(printlog==1):
                    print "Wrong"


        print "Result:"
        print "Correct: ", cnt_correct
        print "Wrong  : ", cnt_wrong



if __name__ == "__main__":
    
    #pos tagging task example
    trainset = [[[ "N", "V", "N" ], ["I", "like", "computer"]],
                [[ "N", "V", "N", "COJ", "N" ], ["He", "love", "computer", "and", "math"]]]

    model = HMM(["N","V","COJ"],["I","like","computer","He","love","math","and"])
    model.train(trainset)
    res = model.calculate(["I","love","math","and","computer"])
    print res


