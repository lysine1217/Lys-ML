# -*- coding: utf-8 -*-

"""
Data Spliter
"""

import random


def data_spliter(dataset=None, prop=[0.8, 0.2, 0.0], shuffle=False):

    """
    Split data into three(two) parts
    
    Training dataset ( default 80% )
    Validate dataset ( default 20% )
    test dataset( default 0% )
    
    """

    train_threshold    = prop[0]
    validate_threshold = prop[0] + prop[1]
    test_threshold     = prop[0] + prop[1] + prop[2]


    train_lst    = []
    validate_lst = []
    test_lst     = []

    if shuffle == True:
        random.shuffle(dataset)


    for i in xrange(len(dataset)):
        r = random.random()
        if r < train_threshold:
            train_lst.append(dataset[i])
        elif r < validate_threshold:
            validate_lst.append(dataset[i])
        else:
            test_lst.append(dataset[i])


    return train_lst, validate_lst, test_lst

    
        
    
    

        
        
