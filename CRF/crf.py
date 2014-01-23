#!/usr/bin/python
#
# Conditional Random Field
# 
#  Description:
#   
#   First Order Markov Model
#   Impelementation is not finished yet
#

import numpy as np


class CRF:

    # features should be set into following format
    # features = [ [("L-0", "word1"), ("L-1","word2"), ("W-2", "word3"), ("W+3", "word4") ] //feature 1
    # L-0 means labels for the current place, W+3 means word whose index equals current index + 3
 
    def __init__(self, labels, features=[]):

        self.labels       = lables
        self.raw_features = features
        self.w            = np.random.random(len(features))
        self.feature      = []

        # set each feature into [[(-1, "word"),(0,"word")] <= information for label
        #                        [(-3, "word"),(0,"word"),(1,"word")] <= information for sequence
        #                       ]
        
        for feature in self.raw_features:
            lab_feature = []
            seq_feature = []
            for (label, word) in feature:
                if label[0] == "L":
                    nlab = int(lable[1:])
                    lab_feature.append((nlab, word))
                else:
                    nlab = int(label[1:])
                    seq_feature.append((nlab, word))
            self.feature.append([lab_feature, seq_feature])
            

    # count how many times a specific feature appears in data

    def feature_count(self, feature, data):

        cnt = 0.0
        lab_feature = feature[0]
        seq_feature = feature[1]
        ld  = len(data)

        for i in xrange(ld):
            flag = 1
            for p, w in lab_feature:
                if (i+p < 0 or i+p >= ld or data[i+p][0] != w):
                    flag = 0
                    break

            for p, w in seq_feature:
                if (i+p < 0 or i+p >= ld or data[i+p][1] != w):
                    flag = 0
                    break
            cnt += flag

        return cnt

    # sum over all labels 

    def sum_feature_count(self, feature, data):
        
        cnt = 0.0
        seq_feature = feature[1]
        ld  = len(data)

        # almost same as the previous function, just ignore lab_feature
        
        for i in xrange(ld):
            for p, w in seq_feature:
                if (i+p <0 or i+p >= ld or data[i+p][1] != w):
                    break
            cnt += forward_backward()
                    

    # dataset should be set into following format
    # dataset = [[(label1, word1),(label2, word2) ..]   //data 1
    #            [(label1, word1),(label2, word2) ..]   //data 2
    #           ]

    def train(dataset, iterations=10, rate=0.05):

        if(len(features)==0):
            print "Set feature before training"
            return

        
        for ii in xrange(iterations):
            
            n_w = np.zeros(len(features))

            # calculate gradient of wi 
            for i, feature in enumerate(self.features):

                # first part
                n_w[i] += np.sum([self.feature_count(feature, data) for data in dataset])

                # second part
                n_w[i] += np.sum([self.sum_feature_count(feature, data) for data in dataset])
        
