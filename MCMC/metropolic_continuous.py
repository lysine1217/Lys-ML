'''
This program is to sampling from the following distribution

p(x1,x2) = 1/Z * exp(-0.5 * (x1^2-2*b*x1*x2+x2^2))

'''

import numpy as np
import sys

xlst = []
ylst = []

def pdf(x1,x2):
    return np.exp(-0.5*(x1**2-x1*x2+x2**2))

def main(iterations):
    x1 = 0.0
    x2 = 0.0

    std = 0.5

    for ii in xrange(iterations):
        d1 = np.random.normal(0.0,std)
        d2 = np.random.normal(0.0,std)

        if(pdf(x1+d1,x2+d2)/pdf(x1,x2) > np.random.random()):
            x1 = x1 + d1
            x2 = x2 + d2

            xlst.append(x1)
            ylst.append(x2)

if __name__ == "__main__":
    main(int(sys.argv[1]))
    
    

    
