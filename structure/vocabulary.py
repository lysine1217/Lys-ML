#-*- coding: utf-8 -*-

"""
Vocabulary
"""
import os
import heapq
from collections import defaultdict
import numpy as np

import lyspy.data.en


class Vocabulary:

    """
    Vocabulary is a data structure to save the basic word level information.
    It can used to process sentences to transform them into integers or vectors

    """    

    def __init__(self, v=None, stopwords=None):
        """
        Initialize vocabularies and stopwords
        """

        # word index, vector, postag
        self.word2dex = dict()
        self.dex2word = dict()

        self.word2vec = dict()
        self.word2tag = dict()

        self.wordnum  = 0

        if v!= None:
            self.set_vocabulary(v)


        self.is_stopword = dict()
        
        if stopwords != None:
            self.set_stopword(stopwords)


        """
        Optional Word Information

        - cnt: counts for each word ( may be used in tfidf )
        - word2vec: word vectors ( may be used in semantic composition )

        """

        self.wordcnt  = defaultdict(int)
        self.word2vec = dict()


    def __len__(self):
        """
        return number of words in vocabulary
        TODO:
        - wordnum are not set currently

        """
        return self.wordnum

        

    def __getitem__(self, sth):

        """
        Get item method just change word and its index currently

        """

        if isinstance(sth, str) :
            if sth in self.word2dex:
                return self.word2dex[sth]
            else:
                return -1
        elif isinstance(sth, int):
            if sth in self.dex2word:
                return self.dex2word[sth]
            else:
                return -1
        else:
            return -1


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



    def get_vector(self, word):
        if self.word2vec.has_key(word):
            return self.word2vec[word]
        else:
            return -1

    def get_postag(self, word):
        if self.word2tag.has_key(word):
            return self.word2tag[word]
        else:
            return "N"


    def read_vectors(self, filepath=None):

        """
        Read default vectors saved in data/en/
        """

        if filepath==None:
            filepath = os.path.join(os.path.dirname(lyspy.data.en.__file__), "vectors.txt")
            
        f = open(filepath, "r").readlines()
        for line in f:
            line = line.split()
            word = line[0]
            vec  = map(float, line[1:])
            self.word2vec[word] = vec


        self.wordvec_pair = self.word2vec.items()

    def read_postags(self, filepath=None):
        """
        Read default postags saved in data/en
        """

        if filepath==None:
            filepath = os.path.join(os.path.dirname(lyspy.data.en.__file__), "postag.txt")
            
        f = open(filepath, "r").readlines()
        for line in f:
            line = line.split()
            if len(line)>=2:
                word = line[0]
                tag  = line[1]
                self.word2tag[word] = tag

    def read_vocabulary(self, filepath=None):
        
        """
        Read default vocabularies
        """

        if filepath==None:
            filepath = os.path.join(os.path.dirname(lyspy.data.en.__file__), "long_frequent_words")

        f = map(str.strip, open(filepath, "r").readlines())
        self.set_vocabulary(f)

    def find_nearest_word(self, val, tag=None):
        """
        return the word that has the nearest vector with "val"
        """

        max_word     = ""
        max_distance = -100000000.0

        for word, vec in self.word2vec.items():
            # check whether postag of word is startswith tag
            if tag == None or self.get_postag(word).startswith(tag):
                distance = np.dot(vec, val)
                if distance > max_distance:
                    max_word = word
                    max_distance = distance

        return max_word

    def find_nearest_euclid_word(self, val, tag=None):

        min_word     = ""
        min_distance = 100000000.0

        for word, vec in self.word2vec.items():
            # check whether postag of word is startswith tag
            if tag == None or self.get_postag(word).startswith(tag):
                v = np.array(vec) - np.array(val)
                distance = np.linalg.norm(v)
                if distance < min_distance:
                    min_word = word
                    min_distance = distance

        return min_word


    def find_nearest_words(self, val, k, tag=None):
        """
        return top k (word, similarity) that has the nearset vector with val
        similarity is cosine similarity

        """

        max_words     = [""]*k
        max_distance  = [-10000000000.0]*k

        for word, vec in self.word2vec.items():

            if tag == None or self.get_postag(word).startswith(tag):

                distance = np.dot(vec, val)
                if distance > max_distance[0]:

                    max_distance[0] = distance
                    max_words[0]    = word

                    # swap sort
                    for i in xrange(k-1):
                        if max_distance[i] > max_distance[i+1]:
                            max_distance[i], max_distance[i+1] = max_distance[i+1], max_distance[i]
                            max_words[i], max_words[i+1] = max_words[i+1], max_words[i]


        return max_words, max_distance

    def find_nearest_euclid_words(self, val, k, tag=None):

        """
        return top k (word, similarity) that has the nearset vector with val
        similarity is cosine similarity

        """

        min_words     = [""]*k
        min_distance  = [10000000000.0]*k

        for word, vec in self.word2vec.items():

            if tag == None or self.get_postag(word).startswith(tag):
                v = np.array(vec) - np.array(val)

                distance = np.linalg.norm(v)
                if distance < min_distance[0]:

                    min_distance[0] = distance
                    min_words[0]    = word

                    # swap sort
                    for i in xrange(k-1):
                        if min_distance[i] < min_distance[i+1]:
                            min_distance[i], min_distance[i+1] = min_distance[i+1], min_distance[i]
                            min_words[i], min_words[i+1] = min_words[i+1], min_words[i]

        return min_words, min_distance

        



    def find_nearest_order(self, val, word):
        """
        return the distance order between val and vector of word
        """

        distance = np.dot(val, self.word2vec[word])
        cnt      = 0

        for vec in self.word2vec.values():
            n_distance = np.dot(vec, val)
            if n_distance > distance:
                cnt += 1

        return cnt

    def find_nearest_euclid_order(self, val, word):
        """
        return the distance order between val and vector of word
        """

        distance = np.linalg.norm(val - self.word2vec[word])
        cnt      = 0

        for vec in self.word2vec.values():
            v = np.array(vec) - np.array(val)
            n_distance = np.linalg.norm(v)
            if n_distance < distance:
                cnt += 1

        return cnt


        
    def process(self, doc, cap=0):

        """
        This function counts words in the documents
        and register words that did not appear before
        
        """

        for wd in doc:
            if wd in self.is_stopword:
                continue

            if wd not in self.word2dex:
                self.word2dex[wd] = self.wordnum
                self.dex2word[self.wordnum] = wd
                self.wordnum += 1

            self.wordcnt[wd] += 1


    def transform(self, doc):
        
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
                    

                
            
            
        
        
