#!/usr/bin/python
#
# Naive Bayes Classifier
#
# All inputs files should be transformed into number
# use Vocabulary module when dealing with language
#

import numpy as np

class NaiveBayes:

    def __init__(self, nc, nv):
        
        # number of class and vocabularies
        self.nc    = nc
        self.nv    = nv

        # probability of class 
        self.pc    = np.zeros(nc)
        
        # probability of vocabulary for each class
        self.pv    = np.zeros([nc, nv])


    # Training documents should be reformed into following format
    # documents = [[[<word1 in doc1>, <word2 in doc1>, <word3 in doc1> ], <class for doc1>],
    #              [[<word1 in doc2>, <word2 in doc2>, <word3 in doc2> ], <class for doc2>],
    #              ...]
    # all words and class should be represented in number !

    def train(self, documents, wordsmoothing=self.nv):

        doclen = len(documents)
        

        # calculate counts for each class and words
        for doc in documents:
            wlst = doc[0]
            cls = doc[1]

            self.pc[cls] += 1
            for word in wlst:
                self.pv[cls][word] += 1

        # calculate word probability and do smoothing
        for cls in xrange(self.nc):
            for word in xrange(self.nv):
                self.pv[cls][word] = (self.pv[cls][word]+1.0)/(self.pc[cls]+smoothing)
                

        # calculate probability for class
        sm = np.sum(self.pc)
        self.pc /= sm


    # Predict documents should be reformed into following format
    # documents = [[<word1 in doc1>, <word2 in doc1> ... ], [<word1 in doc2>, <word2 in doc2>]]

    def predict(self, documents):

        res = [0]*(len(documents))

        for i, doc in enumerate(documents):
            clsprob = np.copy(self.pc)

            for cls in xrange(self.nc):
                for word in doc:
                    clsprob[cls] = clsprob[cls]*self.pv[cls][word]
                              
            res[i] = np.argmax(clsprob)
        


    # test documents should be set into same format as training documents
    def test(self, documents):
        
        predict_documents = [ doc[0] for doc in documents ]
        predict_answer    = [ doc[1] for doc in documents ]
        predict_result    = self.predict(predict_documents)

        cnt_correct = 0
        cnt_wrong   = 0

        for i in xrange(len(predict_answer)):
            if predict_answer[i] == predict_result:
                print "Correct"
                cnt_correct += 1
            else:
                print "Wrong"
                cnt_wrong +=1

        print "Correct count: ", cnt_correct
        print "Wrong   count: ", cnt_wrong
        print "Precision:     ", cnt_correct*1.0/(cnt_correct+cnt_wrong)



def demo():
    print "Demo: "
    


if __name__ == "__main__":
    demo()
        


