# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Latent Dirichilet Allocation 


import numpy as np


class LDA:
    
    def __init__(self, docs, k, alpha=1.0, beta=1.0, v=5000):

        """
        k: number of topic
        alpha: dirichilet parameter for topic
        beta: dirichilet parameter for words
        v: number of vocabulary
        docs: documents for training
        
        """

        self.docs  = docs
        self.k     = k
        self.alpha = alpha
        self.beta  = beta
        self.v     = v
        self.d     = len(self.docs)

        """
        t_wd: topic for each word in each documents
        t_doc: topic distribution for each documents
        c_t: count of topics in all docs
        c_doc_t: count of topics in each doc

        """

        self.t_doc_wd = []

        self.c_doc_t = np.zeros([self.d, self.k]) + alpha
        self.c_t     = np.zeros(self.k) + beta * v
        self.c_wd_t  = np.zeros([self.v, self.k]) + beta


        """
        Randomize initial parameters

        """

        for m, doc in enumerate(self.docs):
            t_wd                     = []

            for i, wd in enumerate(doc):
                z                    = np.random.randint(0, self.k)
                t_wd.append(z)
                self.c_doc_t[m, z]  += 1
                self.c_t[z]         += 1
                self.c_wd_t[wd, z]  += 1

            self.t_doc_wd.append(np.array(t_wd))


    def inference(self, iterations = 1000):

        for ii in xrange(iterations):
            print "Iterations : ",ii
            for m, doc in enumerate(self.docs):
                print "-- ",ii," Doc :",m
                for i, wd in enumerate(doc):
                    
                    """
                    Discount 1 for current word

                    """

                    t = self.t_doc_wd[m][i]

                    self.c_doc_t[m, t]   -= 1
                    self.c_wd_t[wd, t]   -= 1
                    self.c_t[t]          -= 1

                    p = self.c_doc_t[m]*self.c_wd_t[wd]/self.c_t
                    if i==0:
                        print p

                    z = np.random.multinomial(1, p/p.sum()).argmax()
                    
                    self.t_doc_wd[m][i]     = z
                    self.c_doc_t[m, z]     += 1
                    self.c_wd_t[wd, z]     += 1
                    self.c_t[z]            += 1

                    

    def topic_toprank_words(self, number, dic):

        nc_wd_t = np.copy(self.c_wd_t)
        for i in xrange(len(nc_wd_t)):
            nc_wd_t[i] = nc_wd_t[i]/np.sum(nc_wd_t[i])

        for i in xrange(self.k):
            print "Topic : ",i

            word_lst = np.argsort(nc_wd_t[::, i])[::-1][:number]
            print [dic[wd] for wd in word_lst]

            
        
        

