# -*- coding: utf-8 -*-

""" 
word structure for NLP

"""

class Leaf:


    """
    Leaf is an data structure contains information for a single word

    wrd -> raw word
    dex -> word index in vocabulary (optional)
    pos -> postag (optional)
    vec -> distributional vector trained from deep learning (optional)
    cls -> class labels (optional)
    dep -> dependency list (optional)

    """

    def __init__(self, wrd, dex=None, pos=None, vec=None, cls=None, dep=None):
        
        self.wrd = wrd
        self.dex = dex
        self.pos = pos
        self.vec = vec


    def __str__(self):

        res = ""
        
        if self.wrd != None:
            res.append(self.wrd+" ")

        if self.dex != None:
            self.append(str(self.dex)+" ")

        if self.pos != None:
            self.append(str(self.pos)+" ")

        if self.vec != None:
            self.append(str(self.vec)+" ")

        if self.cls != None:
            self.append(str(self.cls)+" ")

        return res
