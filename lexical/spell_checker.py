#/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Spell Checker:
# 
# Algorithm Description:
#  Build bigram posting list for a specific dictionary(wordlist)
#  For each query, construct the conjunction of posting list using its bigram
#  Delete the possible word in the conjuction list if its jaccard coefficient is small
#  Calculate the edit distance to find the most likely word
#
#


import os
import sys
import collections
import numpy as np

class SpellChecker:

    def __init__(self, wordlist):
        self.wordlist = wordlist

        # the first element is the length of the second element
        self.bidict = collections.defaultdict(list)

        for word in self.wordlist:
            for i in xrange(len(word)-1):
                self.bidict[word[i:i+2]].append(word)

    def correct(self, word):
        
        cntdict = collections.defaultdict(int)
        wlen = len(word)

        # find the conjunction of the postinglist
        for i in xrange(len(word)-1):
            bigram = word[i:i+2]
            for w in self.bidict[bigram]:
                cntdict[w] += 1

        # calculate jaccard coefficient for each word
        candidates = []
        for w, cnt in cntdict.items():
            jaccard = cnt*1.0/(len(w)+wlen-cnt)
            candidates.append([jaccard, w])

        candidates.sort(key=lambda x:-x[0])
        
        # select the top 100 word for candidates
        candidates = candidates[:min(100, len(candidates))]

        # calculate edit distance for top words
        topword = ""
        minedit = 1000000

        for jaccard, w in candidates:
            clen = len(w)
            dp = np.zeros([wlen+1, clen+1])
            for i in xrange(wlen+1):
                dp[i][0] = i

            for i in xrange(clen+1):
                dp[0][i] = i
            for i in xrange(1,wlen+1):
                for j in xrange(1, clen+1):
                    dp[i][j] = min([dp[i-1][j-1]+(word[i-1]!=w[j-1]), dp[i-1][j]+1, dp[i][j-1]+1])

            if(minedit>dp[wlen][clen]):
                minedit = dp[wlen][clen]
                topword = w

        print topword
        return topword


    
