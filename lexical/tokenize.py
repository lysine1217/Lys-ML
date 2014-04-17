# -*- coding: utf-8 -*-


"""
simple sentence tokenizer

"""


from .string_tokenize import *


def tokenize(string_or_listofstring, tolower=False, remove_punctions=False):

    if(isinstance(string_or_listofstring, str)):
        return string_tokenize(string_or_listofstring, tolower, remove_punctions)

    else:
        return [string_tokenize(sentence) for sentence in string_or_listofstring]

