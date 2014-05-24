# -*- coding: utf-8 -*-

"""
Validate
"""

import numpy as np
from pandas import DataFrame, Series
from pylab import *

from lyspy.learn.dataset import DataSet
from lyspy.learn.error_model import *

class Validate:


    """
    Validate is a more complicated module for training, validation and testing
    It can be used to do bias - variance analysis every time.
    It plot bias and variance for every epoch
    """

    def __init__(self, model=None, dataset=None, error_func=square_errors, ratio=[0.8, 0.2, 0.0]):

    	# training model
        self.model      = model

        # dataset
        self.dataset    = dataset
        self.train_dataset, self.validate_dataset, self.test_dataset = self.dataset.split(ratio)

        # inputs and targets of input
        self.train_input  = self.train_dataset.input
        self.train_target = self.train_dataset.target

        # inputs and targets of validate
        self.validate_input  = self.validate_dataset.input
        self.validate_target = self.validate_dataset.target


        # error model
        self.error_func = error_func
        self.binary     = 0

        self.train_errors    = []
        self.validate_errors = []


        if self.error_func == class_errors:
        	self.binary = 1

    def train(self, epoch=1000, each_epoch=1, rate=0.05):

    	"""
    	model debugging
    	It displays errors of both training data and validation data every epoch

    	red point:   train error
    	blue point:  validate error

    	"""

    	for i in xrange(epoch):

    		print "Epoch: ", i

    		# train just one epoch every time
    		self.model.train(self.train_dataset, epoch=each_epoch, rate=rate)

    		# calculate results and errors of training data
    		self.train_result = self.model.predict(self.train_dataset, binary=self.binary) 
    		self.train_error  = self.error_func(self.train_result, self.train_target)
            # self.train_errors.append(self.train_error)


    		# calculate results and errors of validation data
    		self.validate_result = self.model.predict(self.validate_dataset, binary=self.binary)
    		self.validate_error = self.error_func(self.validate_result, self.validate_target)
            # self.validate_errors.append(self.validate_error)

    		# print information of errors
    		print "Train Average Error    :", self.train_error
    		print "Validate Average Error :", self.validate_error
    		print ""

    def plot_curve(self):

        index = range(0, len(self.train_errors))
        scatter(index, self.train_errors, c="R")
        scatter(index, self.validate_errors, c="B")

    def plot_train_curve(self):

        index = range(0, len(self.train_errors))
        scatter(index, self.train_errors, c="R")

    def plot_validate_curve(self):

        index = range(0, len(self.train_errors))
        scatter(index, self.train_errors, c="R")

        
    def compare_train(self, index=None):
        """
        compare training results and targets with detailed information
        it is possible to check specific case by setting index
        """

        if index==None:
            index = range(len(self.train_dataset))
        elif isinstance(index, int):
            index = [index]

        for i in index:
            print "Case "+str(i)+" : "
            print "- train input : ", self.train_input[i]
            print "- train target: ", self.train_target[i]
            print "- train result: ", self.train_result[i]
            print "- train error : ", self.error_func(self.train_target[i], self.train_result[i])
            print ""


    def compare_validate(self, index=None):

        """
        compare training results and targets with detailed information
        it is possible to check specific case by setting index
        """

        if index==None:
            index = range(len(self.validate_dataset))
        elif isinstance(index, int):
            index = [index]

        for i in index:
            print "Case "+str(i)+" : "
            print "- train input : ", self.validate_input[i]
            print "- train target: ", self.validate_target[i]
            print "- train result: ", self.validate_result[i]
            print "- train error : ", self.error_func(self.validate_target[i], self.validate_result[i])
            print ""






