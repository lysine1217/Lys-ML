#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Trie Tree Python Implementation
#
# k childs are available from each parent
#  e.g. English: 26, Japanese: 場合による（カタカナ常用だけなら85)
# offset is to calculate index for each character in utf-8
#  e.g. English: 'a'=97が最小, Japanese ひらがな：12354, カタカナ：12449

import os
import sys
import codecs

class Trie:
    
    k      = 26 # number of alphabet
    offset = 97 # order for alphabet 'a' 

    def __init__(self):
        self.child  = [None]*self.k
        self.exist   = False


    def insert(self, string):
        if(len(string)==0):
            self.exist = True
            return True

        index = ord(string[0])-self.offset
        if(index>=self.k or index<0):
            print "Invalid character found", index, string[0]
            return False

        if(self.child[index] == None):
            self.child[index] = Trie()

        self.child[index].insert(string[1:])

    def search(self, string):
        if(len(string)==0):
            return self.exist

        index = ord(string[0])-self.offset
        if(index>=self.k or index<0):
            print "Invalid character found", index, string[0]
            return False
        if(self.child[index] == None):
            print "Not found"
        else:
            return self.child[index].search(string[1:])


if __name__ == "__main__":
    
    # use following dictinary extracted from ipadic
    lst = map(unicode.split, codecs.open("../../data/midashi_yomi.dic","r","utf_8").readlines())
    Trie.k = 85
    Trie.offset = 12449
    jap_dict = Trie()

    for i, word in enumerate(lst):
        print i
        jap_dict.insert(word[1])
