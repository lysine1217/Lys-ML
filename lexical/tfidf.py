# -*- coding: utf-8 -*-

from lyspy.lexical.tokenize import tokenize
from lyspy.structure.vocabulary import Vocabulary
from lyspy.structure.document import Document

class TFIDF:

    """
    Compute important words in specified text
    or compute word weight

    """

    def __init__(self, doc, refer_doc=None):

        self.doc = Document(doc)
        
