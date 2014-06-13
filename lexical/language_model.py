# -*- coding: utf-8 -*-

"""
Language Model
"""
from collections import defaultdict

import cPickle as pickle
import numpy as np
import math

from lyspy.structure.vocabulary import Vocabulary
from lyspy.structure.sentence import Sentence

class LanguageModel:

    """
    Normal language model
    compute bigram language model in default
    
    param: additive parameter
    
    TODO:
    kneser-ney smoother
    SRILM IO format
    Concise format with Vocabulary compression
    """

    def __init__(self, ngram=2, param=0.0001):

        self.ngram = ngram
        self.param = param

        self.ngramdict = defaultdict(float)
        self.unigramdict = defaultdict(float) 
        self.vcnt  = 0


    def train(self, dataset):
        
        self.dataset   = Sentence(dataset)
        for words in self.dataset.ngrams(self.ngram):
            bigram = " ".join(words)
            self.ngramdict[bigram] += 1.0
            self.unigramdict[words[0]] += 1.0

        self.vcnt = len(self.unigramdict)

        # normalization and smoothing

        for u,v in self.ngramdict.items():
            self.ngramdict[u] = np.log((v+self.param)/(self.unigramdict[u[0]] + self.param*self.vcnt))
        

    def predict(self, dataset):
        
        """
        Return values will be logistic probability
        """

        
        self.testdata = Sentence(dataset)
        self.res = 0.0

        for wlst in self.testdata.ngrams(self.ngram):

            words = " ".join(wlst)

            # constant values will be added if corresponding ngram is 0
            if self.ngramdict[words] == 0.0:
                self.res += np.log(self.param / self.unigramdict[wlst[0]] + self.param*self.vcnt)
            else:
                self.res += self.ngramdict[words]

        return self.res


    def save_model_pickle(self, filepath):

        """
        Current just dump objects into pickle for ease
        """

        
        f = open(filepath, "w")
        pickle.dump([self.unigramdict, self.ngramdict], f)
        f.close()

    def save_model(self, filepath):
        """
        Format:
        unigram cnt, bigramcnt
        w1 w1cnt
        ...
        w1 w2 w1-w2cnt
        ...
        """
        
        f = open(filepath, "w")
        f.write(str(len(self.unigramdict))+" "+str(len(self.ngramdict))+"\n")

        for w, cnt in self.unigramdict.items():
            f.write(w+" "+str(cnt)+"\n")
        
        for w, cnt in self.ngramdict.items():
            f.write(w+" "+str(cnt)+"\n")

        f.close()

    def load_model(self, filepath):
        """
        load the model defined in save_model
        """

        f = open(filepath, "r")
        lines = f.readlines()

        self.vcnt, bicnt = map(int, lines[0].split())

        for i in xrange(1, self.vcnt+1):
            word, cnt = lines[i].split()
            self.unigramdict[word] = float(cnt)

        for i in xrange(self.vcnt+1, len(lines)):
            
            word1, word2, cnt = lines[i].split()
            self.ngramdict[word1+" "+word2] = float(cnt)


    def read_model(self, filepath):
        
        f = open(filepath, "r")
        self.unigramdict, self.ngramdict = pickle.load(f)
        

        
            
            
