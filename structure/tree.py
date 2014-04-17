# -*- coding: utf-8 -*-

"""
Tree structure for NLP
"""

from lyspy.lexical.tokenize import tokenize
from .leaf import Leaf

class Tree:

    """
    Tree is a data structure contains information for a sentence,
    mainly syntactic information currently
    Tree is a substructure of Sentence ( in the future )

    """

    
    def __init__(self, rawtext=None):

        if(rawtext != None):
            self.readfromstring(rawtext)


    def readfromstring(self, rawtext):
        """ 
        read parsed tree
        
        """
        
        self.rawtext  = rawtext
        self.word_lst = tokenize(self.rawtext)
        self.leaf_lst = []

        for word in self.word_lst:
            self.leaf_lst.append(Leaf(word))
