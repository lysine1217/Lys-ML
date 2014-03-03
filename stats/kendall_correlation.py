#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Kendall tau rank correlation coefficient
#
#

def demoKendall():
    
    x = [6,4,5,10,2,8,3,9,1,7]
    y = [10,1,4,9,3,8,6,5,2,7]

    # result should be 0.703

    res = Kendall(x,y)
    print x
    print y
    print "Kendal demo: ", res


def Kendall(x,y=None):

    cnt = len(x)

    if y == None:
        y = range(1,cnt+1)

    for i in xrange(cnt):
        for j in xrange(cnt):
            mark = (x[i]-x[j])*(y[i]-y[j])
            if mark > 0:
                coeff += 1.0
            elif mark < 0:
                coeff -= 1.0

    print coeff

    return coeff/cnt/(cnt-1)
            

    
