#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# List Transform Program
#
#  Description:
#
#   This program is for transformming list files to desired format
#   Mainly for the purpose of range setting and factor setting
#
#   Transform instruction should obey the following format
#   
#   ER(min, max): Explanatory Variable. Range can be set by specifying min and max
#   T: Target Numerical Variable
#   D: Deleted Variable
#   EF(F1,F2,F3): Explanatory Factor Variable. All possible factor should be listed after F, no spaces are allowed inside
#   TF(F1,F2,F3): Target Factor Variable. Same as previous one
#   Example:
#        instruction="E T D EF(male,female)"


import csv
import numpy as np

class Transform():

    def __init__(self, lst=[]):

        # before list and after list
        self.blst = np.array(lst)
        self.alst = np.array([])

        # explanatory variable list and target list
        self.elst = np.array([])
        self.tlst = np.array([])

        # count for cases
        self.nc   = len(self.blst)

    
    # read csv files
    def reader(self, filename, delimit=",", header=0):
        fl = csv.reader(file(filename),delimiter=delimit)
        self.blst = []
        self.alst = np.array([])
        self.elst = np.array([])
        self.tlst = np.array([])

        for line in fl:
            self.blst.append(line)

        for i in xrange(len(self.blst)):
            for j in xrange(len(self.blst[i])):
                if self.blst[i][j]=="":
                    self.blst[i][j] = "0.0"


        # remove header
        if(header==1):
            self.blst = np.array(self.blst[1:])


        self.nc = len(self.blst)


    # transform instruction should obey the following format
    # ER(min, max): Explanatory Variable. Range can be set by specifying min and max
    # T: Target Numerical Variable
    # D: Deleted Variable
    # EF(F1,F2,F3): Explanatory Factor Variable. All possible factor should be listed after F, no spaces are allowed inside
    # TF(F1,F2,F3): Target Factor Variable. Same as previous one
    # Example: 
    #        instruction="E T D EF(male,female)"

    def transform(self, instruction):

        instruction = instruction.split()

        # inverse for ease of transformation
        self.blst = self.blst.T

        for i, vlst in enumerate(self.blst):
            ins = instruction[i]

            # ignore the variable if it is D
            if(ins[0] == "D"):
                continue

            if(ins[0] == "E"):
                
                # normal explanatory variable
                if(len(ins)==1 or ins[1]=="R" or ins[1]=="A"):

                    # set specified range
                    if(ins[1]=="R"):
                        vlst = vlst.astype(np.float)
                        min_e, max_e = ins[3:-1].split(",")
                        
                        min_e = float(min_e)
                        max_e = float(max_e)

                        for j, v in enumerate(vlst):
                            vlst[j] = (v-min_e)*1.0/(max_e-min_e)

                    # automatic range
                    if(ins[1]=="A"):
                        min_e = np.min(vlst)
                        max_e = np.max(vlst)

                        for j,v in enumerate(vlst):
                            vlst[j] = (v-min_e)*0.95/(max_e-min_e)

                    if(len(self.elst)==0):
                        self.elst = np.array([vlst])
                    else:
                        self.elst = np.append(self.elst, [vlst], axis=0)

                # factor explanatory variable
                else:

                    factor = ins[3:-1].split(",")
                    lf     = len(factor)
                    flst   = np.zeros([lf, self.nc])

                    for j, v in enumerate(vlst):
                        for k, f in enumerate(factor):
                            if f == v:
                                flst[k][j] = 1.0
                                break

                    if(len(self.elst)==0):
                        self.elst = np.array(flst)
                    else:
                        self.elst = np.append(self.elst, flst, axis=0)



            # target variable
            if(ins[0]=="T"):
                
                if(len(ins)==1 or ins[1]=="R" or ins[1]=="A"):

                    # TR(min, max)
                    if(len(ins)>1 and ins[1]=="R"):
                        vlst = vlst.astype(np.float)
                        min_t, max_t = ins[3:-1].split(",")

                        min_t = float(min_t)
                        max_t = float(max_t)

                        for j, v in enumerate(vlst):
                            vlst[j] = (v-min_t)*1.0/(max_t-min_t)

                    # TA automatic range
                    if(len(ins)>1 and ins[1]=="A"):
                        vlst = vlst.astype(np.float)
                        min_t = np.min(vlst)
                        max_t = np.max(vlst)

                        for j, v in enumerate(vlst):
                            vlst[j] = (v-min_t)*0.95/(max_t-min_t)


                    if(len(self.tlst)==0):
                        self.tlst = np.array([vlst])
                    else:
                        self.tlst = np.append(self.tlst, [vlst],axis=0)
                else:
                    factor = ins[3:-1].split(",")
                    lf     = len(factor)
                    flst   = np.zeros([lf, self.nc])
                    
                    for j, v in enumerate(vlst):
                        for k, f in enumerate(factor):
                            if f == v:
                                flst[k][j] = 1.0
                                break

                    if(len(self.tlst)==0):
                        self.tlst = np.array(flst)
                    else:
                        self.tlst = np.append(self.tlst, flst, axis=0)


        # inverse back
        self.elst = np.array([np.array(lst, dtype=np.float) for lst in self.elst])
        self.tlst = np.array([np.array(lst, dtype=np.float) for lst in self.tlst])

        self.elst = self.elst.T
        self.tlst = self.tlst.T

        # append explanatory and target variables to rlst
        if(len(self.tlst)==0):
            self.alst = np.array(self.elst, dtype=np.float)
        else:
            self.alst = np.array(zip(self.elst, self.tlst))

        return self.alst
        
    

    
if __name__ == "__main__":
    
    t = Transform()
    t.reader("./train.csv",header=1)
    #rlst = t.transform("D T EF(1,2,3) D EF(male,female) ER(0,100.0) E E D ER(0,100.0) D EF(C,Q,S)")
    rlst = t.transform("D T EF(1,2,3) D EF(male,female) ER(0,50.0) D D D D D D")
                  
