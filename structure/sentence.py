# -*- coding: utf-8 -*-

"""
Sentence
"""

from lyspy.lexical.tokenize import tokenize
from lyspy.structure.vocabulary import Vocabulary


class Sentence:

    """
    Sentence defines sentence structures, this will be a container for any nlp processing

    Essential features:
    - Sentence.raw
    - Sentence.words
    
    TODO:
    Optional features (will be implemented in the feature)
    - Sentence.postag
    - Sentence.parse
    - Sentence.dependency
    """

    def __init__(self, string_or_listofwords):


        if isinstance(string_or_listofwords, str):
            self.raw   = string_or_listofwords
            self.words = tokenize(self.raw)

        else:

            self.raw   = " ".join(string_or_listofwords)
            self.words = string_or_listofwords


        self.pos   = None
        self.tree  = None
        self.dep   = None
        self.dex   = None   

    def __str__(self):

        return self.raw

    def __len__(self):
        return len(self.words)

    def __getitem__(self, sth):

        return self.words[sth]

    def __setitem__(self, sth, word):
        self.words[sth] = word


    def index(self, v, remove_nomap_word = True):
        
        """
        Change all words in v to its index registered in v

        if remove_nomap_word is set to True, all words 
        
        """

        if self.dex!=None:
            return 
        
        self.dex = []

        for word in self.words:
            word_dex = v[word]

            if word_dex == -1 and remove_nomap_word == True:
                continue

            self.dex.append(word_dex)
            
    def ngrams(self, n=2):
        res = []
        for i in xrange(len(self.words)-n+1):
            n_ngram = []
            for j in xrange(n):
                n_ngram.append(self.words[i+j])
            res.append(n_ngram)

        return res

