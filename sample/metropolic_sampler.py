# -*- coding: utf-8 -*-

'''
Metropolic Sampler

This program is based on the first chapter of computational statistics 2

Sampling from the following distribution
P(x1,x2,x3) = exp(theta*x1*x2 + theta*x2*x3 + theta*x1*x3)/Z

'''

import sys
import numpy as np

def metropolic_sampler():

    def f(theta,y):
        return np.exp(theta*y[0]*y[1]+theta*y[1]*y[2]+theta*y[2]*y[0])
    
    x   = [1]*3
    cnt = [0]*8
    mean = 0.0

    iterations = int(sys.argv[1])
    theta      = float(sys.argv[2])

    for ii in xrange(iterations):
        ni = np.random.randint(0,3)
        nx = [x[0],x[1],x[2]]
        nx[ni] *= -1
        
        r1 = f(theta, nx)
        r2 = f(theta,x)
        r = r1/r2

        if(np.random.random()<r):
            x = nx
            cnt[(x[0]==1)*4+(x[1]==1)*2+(x[2]==1)] += 1
        else:
            cnt[(x[0]==1)*4+(x[1]==1)*2+(x[2]==1)] += 1
        mean += x[0]*x[1]
        
        if(ii %( iterations/10)==0):
            print mean/(ii+1)

    for i in xrange(8):
        print i," : ",cnt[i]
    

