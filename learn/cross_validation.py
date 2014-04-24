# -*- coding: utf-8 -*-

"""
Cross Validation Model
"""

from lyspy.test.data_spliter import data_spliter

class CrossValidation:

    """
    Use train dataset, validate dataset, test dataset

    Current version is just a prototype

    """
    
    def __init__(self, f, dataset):

        train_lst, validate_lst, test_lst = data_spliter(dataset)
        f.train(train_lst)
        f.test(validate_lst)
        f.test(test_lst)



        
