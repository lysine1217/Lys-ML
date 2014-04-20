# -*- coding: utf-8 -*-

"""
Language Model
"""
from collections import defaultdict

import cPickle as pickle
import numpy as np

from lyspy.structure.vocabulary import Vocabulary
from lyspy.structure.sentence import Sentence

class LanguageModel:

    """
    Normal language model
    compute bigram language model in default
    
    TODO:
    kneser-ney smoother
    SRILM IO format
    Concise format with Vocabulary compression
    """

    def __init__(self, ngram=2):

        self.ngram = 2
        self.ngramdict = default(float)
        self.unigramdict = default(int) 

    def train(self, dataset):
        
        self.dataset   = Sentence(dataset)
        for words in self.dataset.ngram(self.ngram):
            self.ngramdict[words] += 1.0
            self.unigramdict[words[0]] += 1.0


        # normalization (no smoothing currently)

        for u,v in self.ngramdict.items():
            self.ngramdict[u] = v/(self.unigramdict[u[0]])
        

    def predict(self, dataset):
        
        """
        Return values will be logistic probability
        """

        
        self.testdata = Sentence(dataset)
        self.res = 0.0

        for u,v in self.testdata.ngram(self.ngram):

            # constant values will be added if corresponding ngram is 0
            if self.ngramdict[words] == 0.0:
                self.res += np.log(0.0001)
            else:
                self.res += np.log(self.ngramdict[words])


        return self.res


    def save_model(self, filepath):

        """
        Current just dump objects into pickle for ease
        """

        
        f = open(filepath, "w")
        pickle.dump([unigramdict, ngramdict], f)
        f.close()


    def read_model(self, filepath):
        
        f = open(filepath, "r")
        self.unigramdict, self.ngramdict = pickle.load(f)
        

        
            
            
