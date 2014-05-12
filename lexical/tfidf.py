# -*- coding: utf-8 -*-

# standard library
import operator
from collections import defaultdict
import numpy as np


# lyspy library
from lyspy.lexical.tokenize import tokenize
from lyspy.structure.vocabulary import Vocabulary
from lyspy.structure.document import Document

class TFIDF:

    """
    Compute important words in specified text
    or compute word weight

    """

    def __init__(self):
        self.doc = None
        self.docs = None
        self.nd  = 0

        self.ws  = defaultdict(set)

        self.tf  = defaultdict(float)
        self.idf = defaultdict(float)

        self.tfidf = dict()


    def train_idf_depreciated(self, rdocs):
        """
        default definition of idf
        r_docs should be a list of documents

        """

        self.rdocs = [Document(rdoc) for rdoc in rdocs]
        self.nd     = len(self.rdocs)

        # use set to calculate how many documents contains each word
        for i, rdoc in enumerate(self.rdocs):
            for word in rdoc.words:
                self.ws[word].add(i)


        # calculate the size of each set
        for word, ws in self.ws.items():
            self.idf[word] = len(ws)



    def train_idf(self, rdocs):


        # easy approximation of idf
        
        self.rdocs = Document(rdocs)
        for word in self.rdocs.words:
            self.idf[word] += 1

        self.nd = len(self.rdocs)
            
        
    def train_tf(self, doc):
        
        """
        doc should be a document
        """

        self.doc = Document(doc)

        for word in self.doc.words:
            # calcuate frequency for each word
            self.tf[word] += 1
            


    def predict_word_weight(self, word):

        """
        return tfidf weight for word
        if idf or tf is 0 return -1
        
        """

        if self.tfidf.has_key(word):
            return self.tfidf[word]
        else:
            if self.tf[word]==0 or self.idf[word]==0:
                self.tfidf[word] = -1
                return -1
        
            else:
                self.tfidf[word] = self.tf[word]*np.log(self.nd/self.idf[word])
                return self.tfidf[word]
            

    def top_weight_words(self, n):
        
        self.topwords = []
        

        # for all words in tf, calculate its weight
        for word in self.tf.keys():
            if self.tfidf.has_key(word):
                if self.tfidf[word] == -1:
                    continue
                else:
                    self.topwords.append((word, self.tfidf[word]))
            else:
                if self.tf[word] == 0 or self.idf[word] == 0:
                    self.tfidf[word] = -1
                    continue

                else:
                    self.tfidf[word] = self.tf[word]*np.log(self.nd/self.idf[word])
                    self.topwords.appedn((word, self.tfidf[word]))

                                         
                
        # sort words by tfidf value

        self.topwords.sort(key=operator.itemgetter(1), reverse=True)


        # print top n words and their weight

        return self.topwords[:(min(n, len(self.topwords)))]
