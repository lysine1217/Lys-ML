#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Support Vector Machine
#
# Description:
#  
#  This svm is soft-margin svm
#  and implemented based on SMO algorithm
#
# Dependency:
#
#  numpy
#  

import numpy as np

class SVM:


    # k is the number of the class
    # k = 2 (binary classification) in the case of default setting
    # c is the parameter controlling the penality of mistakes
    # svm is a hard-margin svm when c is infinity

    def __init__(self, kernel=None, k=2, c=10000):
        self.k = k
        self.c = c
        self.kernel = kernel
        if(self.kernel == None):
            self.kernel = self.gaussKernel

        
    # Kernel can be set here
    #
    #

    def linearKernel(self,v1,v2):
        return np.dot(np.array(v1),np.array(v2))

    def gaussKernel(self, v1, v2, sd=100):
        v1 = np.array(v1)
        v2 = np.array(v2)

        return np.exp(-((np.linalg.norm(v1-v2)/sd)**2))

    

    # The label is calculated by following formula
    # f(x) = b + sum (ai*yi*kernel(xi,x)) // i sums over all dataset
    #
    def calc(self, data):

        res = self.b

        for i in xrange(self.n):
            res += self.dataset[i][1]*self.a[i]*self.kernel(self.dataset[i][0],data)

        return res


    # training dataset should be set in following format
    # dataset = [[[v1, v2, v3], l1],
    #            [[v1, v2, v3], l2],
    #            ...]
    # lable should be {1,-1}
    # variables can be set in any format as long as corresponding kernel exists
    #


    def train(self, dataset,  iterations=10000):
        
        self.n       = len(dataset)
        self.dataset = dataset
        self.a       = np.zeros(self.n)  # lagrange multiplier
        self.b       = 0                 # threshold

        for ii in xrange(iterations):

            # number for change
            num_change = 0
            
            # select xi, the first smo parameter
            for i in xrange(self.n):

                xi = self.dataset[i][0]
                yi = self.dataset[i][1]
                
                # calculate ei = f(xi) - label(xi)
                ei = self.calc(xi) - yi

                # check violations of KKT
                violation = False

                if(self.a[i] < self.c and ei*yi < -0.0001):
                    violation = True

                if(self.a[i] > 0 and ei*yi > 0.0001):
                    violation = True

                # skip xi if no violations
                if(not violation):
                    continue


                # select j != j randomly for the second smo parameter
                j = np.random.randint(0, self.n)
                while(i==j):
                    j = np.random.randint(0, self.n)

                xj = self.dataset[j][0]
                yj = self.dataset[j][1]

                # calculate ej = f(xj) - label(xj)
                ej = self.calc(xj) - yj

                ai = self.a[i]
                aj = self.a[j]

                # calculate L and H for xj , constraints for xj

                L = 0
                H = 0
                
                if(yi == yj):
                    L = max(0, ai + aj - self.c)
                    H = min(ai + aj, self.c)
                else:
                    L = max(0, aj - ai)
                    H = min(self.c, self.c + aj - ai)

                # continue if L == H

                if(L == H):
                    continue

                # calculate eta for renewal
                eta = 2.0 * self.kernel(xi,xj) - self.kernel(xi,xi) - self.kernel(xj,xj)

                if(eta >= 0.0):
                    continue

                # renewal aj with clipping
                n_aj = aj - yj*(ei-ej)/eta

                if(n_aj > H):
                    self.a[j] = H
                elif(n_aj < L):
                    self.a[j] = L
                else:
                    self.a[j] = n_aj


                # continue if aj does not change much
                if(abs(self.a[j] - aj) < 0.0001):
                    continue

                # renewal ai
                self.a[i] = self.a[i] + yi*yj*(aj - self.a[j])

                # renewal threshold b
                b1 = self.b - ei - yi*(self.a[i] - ai)*self.kernel(xi,xi)-yj*(self.a[j]-aj)*self.kernel(xi,xj)
                b2 = self.b - ej - yi*(self.a[i] - ai)*self.kernel(xi,xj)-yj*(self.a[j]-aj)*self.kernel(xj,xj)


                if(self.a[i] < self.c):
                    self.b = b1
                elif(self.a[j] < self.c):
                    self.b = b2
                else:
                    self.b = (b1 + b2)/2.0

                
                num_change += 1
                
            if(num_change == 0):
                print "converge"
                break


    # dataset should be set into following format
    # dataset = [[v1,v2,v3,..] , [v1,v2,v3,...],...]

    def predict(self, dataset, binary=1):

        res = []

        for i in xrange(len(dataset)):
            x = dataset[i]
            r = self.calc(x)
            if(binary==1):
                if(r>0.0):
                    res.append(1)
                else:
                    res.append(0)
            else:
                res.append(r)

        return res

    # dataset should be set into following format
    # dataset = [[[v1,v2,v3,..], l1],
    #            [[v1,v2,v3,..], l2],
    #            ...]

    def test(self, dataset):

        cnt_correct = 0
        cnt_wrong   = 0
        
        for i in xrange(len(dataset)):

            x = dataset[i][0]
            y = dataset[i][1]

            if(self.calc(x)*y>0):
                print "Correct"
                cnt_correct += 1
            else:
                print "Wrong"
                cnt_wrong += 1

        print "Correct: ", cnt_correct
        print "Wrong:   ", cnt_wrong

            


if __name__ == "__main__":

    # following dataset is about acceptance desicion of applicants
    # explaining variables are scores of examination and interview
    # target variable is whether the specific applicant are successful

    acceptance = [[[68,65],1],[[85,80],1],
                  [[50,95],1],[[54,70],1],
                  [[66,75],1],[[35,55],-1],
                  [[56,65],-1],[[25,75],-1],
                  [[43,50],-1],[[70,40],-1]]


    # number of explaining variables are 2
    svm = SVM()
    svm.train(acceptance)
    svm.test(acceptance)
