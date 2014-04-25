#-*- coding: utf-8 -*-

"""
Vocabulary
"""

from collections import defaultdict

import numpy as np


class Vocabulary:

    """
    Vocabulary is a data structure to save the basic word level information.
    It can used to process sentences to transform them into integers or vectors

    """    

    def __init__(self, v=None, stopwords=None):

        """
        Set vocabularies
        """

        self.word2dex = dict()
        self.dex2word = dict()

        if v!= None:
            self.set_vocabulary(v)

        """
        Set stopwords

        """
        self.is_stopword = dict()
        
        if stopwords != None:
            self.set_stopword(stopwords)


        """
        Optional Word Information

        - cnt: counts for each word ( may be used in tfidf )
        - word2vec: word vectors ( may be used in semantic composition )

        """

        self.cnt = defaultdict(int)
        self.word2vec = dict()
        

    def __getitem__(self, sth):
        if isinstance(sth, str) :
            if sth in self.dic_words:
                return self.dic_words[sth]
            else:
                return -1
        elif isinstance(sth, int):
            if sth>=0 and sth < len(self.frq_words):
                return self.frq_words[sth]
            else:
                return False
        else:
            return False


    def set_vocabulary(self, v):

        if isinstance(v, list):
            for i, w in enumerate(v):
                self.word2dex[w] = i
                self.dex2word[i] = w

        if isinstance(v, dict):
            for i, w in enumerate(v.keys()):
                self.word2dex[w] = i
                self.dex2word[i] = w
            

    def set_stopwords(self, stopwords):
        for word in stopwords:
            self.is_stopword[word] = True


    def set_vectors(self, vectors=None):

        
    # param cap : ignore the captalization when cap = 0
    #
    # This func counts words in the documents
    # and set the most frequent v words into indexes

    def process_documents(self, docs, cap=0):

        for doc in docs:
            for wd in doc:

                if cap == 0:
                    wd = wd.lower()

                if wd in self.dic_stopwords:
                    continue
                if wd in self.cnt_words:
                    self.cnt_words[wd] += 1
                else:
                    self.cnt_words[wd] = 1

        self.frq_pairs = sorted(self.cnt_words.items(), key=lambda x:-x[1])
        self.frq_words = [wd[0] for wd in self.frq_pairs]
        
        if(len(self.frq_words) > self.v):
            self.frq_words = self.frq_words[:self.v]

        for i, wd in enumerate(self.frq_words):
            self.dic_words[wd] = i


    def read_nonstopwords(self, nonstopwords=None):

        # read nonstop words from data dir 
        # if nonstopwords does not exist

        if nonstopwords == None:
            nw = file("../data/en/top1000_nostop.txt").readlines()
            nonstopwords = map(str.strip, nw)
            self.v = len(nonstopwords)

        
        self.frq_words = nonstopwords
        if len(self.frq_words) > self.v:
            self.frq_words = self.frq_words[:self.v]

        for i, wd in enumerate(self.frq_words):
            if wd not in self.dic_words:
                self.dic_words[wd] = i


    def print_top_words(self, v=None):

        if v == None:
            v = self.v

        for i in xrange(v):
            print self.frq_words[i]
        

    def transform_documents(self, docs):
        
        lst_result = []
        for doc in docs:
            lst_wd = []
            for wd in doc:
                if wd in self.dic_words:
                    lst_wd.append(self.dic_words[wd])
                else:
                    continue
            lst_result.append(lst_wd)
        return lst_result
                    

                
            
            
        
        
