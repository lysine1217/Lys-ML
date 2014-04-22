# -*- coding: utf-8 -*-

"""
sentence
"""

from lyspy.lexical.tokenize import tokenize
from lyspy.lexical.tokenize import Vocabulary


class Sentence:

    """
    Sentence defines sentence structures, this will be a container for any nlp processing

    Essential features:
    - Sentence.raw
    - Sentence.words
    
    Optional features (will be implemented in the feature)
    - Sentence.postag
    - Sentence.parse
    - Sentence.dependency
    """

    def __init__(self, string_or_listofstrings):

        if isinstance(string_or_listofstring, string):
            self.raw   = string_or_listofstring
            self.words = tokenize(self.raw)

        else:
            self.raw   = " ".join(string_or_listofstring)
            self.words = tokenize(self.raw)

        self.pos   = None
        self.tree  = None
        self.dep   = None
        self.dex   = None   

    def __str__(self):

        return self.raw

    def __getitem__(self, sth):

        return self.words[sth]


    def index(self, v, remove_nomap_word = True):
        
        """
        Change all words in v to its index registered in v

        if remove_nomap_word is set to True, all words 
        
        """

        if self.dex!=None:
            
        
        self.dex = []

        for word in self.words:
            word_dex = v[word]

            if word_dex == -1 and remove_nomap_word == True:
                continue

            self.dex.append(word_dex)
            
        

        
