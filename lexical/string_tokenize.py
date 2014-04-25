# -*- coding: utf-8 -*-

"""
simple string spliter

"""

def string_tokenize(sentence, tolower=False, remove_punctions=False):

    """
    This split string into words all typical punctions* will be removed if remove_punction is set true
    Examples:
    - string_tokenize("I want to sleep!") -> ["I", "want", "to", "sleep","!"]
    - string_tokenize("I want $100000 dollars!!!") -> ["I", "want", "$", "1000000", "dollars", "!","!","!"]

    * typical punctions is defined as followings.
    ascii 33 ~ 47 ! " # $ % & ' ( ) * + , -. /
    ascii 58 ~ 64 : ; < = > ? @

    """


    word_lst  = []
    word_start = False
    word_start_point = 0

    if tolower==True:
        sentence = sentence.lower()
    

    for i in xrange(len(sentence)+1):
        if i==len(sentence):
            if word_start==True:
                word_lst.append(sentence[word_start_point:i+1])
                word_start = False
            break

        if str.isspace(sentence[i]):
            if word_start == True:
                word_lst.append(sentence[word_start_point:i])
                word_start = False

        ascii_num = ord(sentence[i])
        if (ascii_num >= 33 and ascii_num <= 47) or (ascii_num >= 58 and ascii_num <= 64):
            if word_start == True:
                word_lst.append(sentence[word_start_point:i])

            if remove_punctions == False:
                word_lst.append(sentence[i:i+1])

            word_start = False

    
        if str.isalnum(sentence[i]):
            if word_start == False:
                word_start = True
                word_start_point = i


    return word_lst

        
    

    

    
