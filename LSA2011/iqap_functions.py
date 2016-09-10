#!/usr/bin/env python

"""
Functions for analyzing the IQAP data and illustrating how iqap.py works.
"""

__author__ = "Christopher Potts"
__credits__ = []
__version__ = "2.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

######################################################################

import re
from collections import defaultdict
from operator import itemgetter
from iqap import *

######################################################################
## The following are responses to some of the
## questions/hunches/hypotheses that the in-class groups formulated on
## July 12:

#---------------------------------------------------------------------
# Question: Which examples have prefixes?

def classification_by_prefixed():
    """Shows how the prefixes are distributed across the source types."""
    d = defaultdict(int)
    iqap = IqapReader('iqap-data.csv')
    for item in iqap.dev_set():
        prefixed = False
        if item.Prefix:
            prefixed = True            
        d[(item.Classification, prefixed)] += 1
    # Printing:
    for key, val in list(d.items()):
        print(key, val)
        
# classification_by_prefixed()    


#---------------------------------------------------------------------
# Question: Are the 'probable' categories chosen more often where the
# answers contain attitude predicates, modals, hedges, additive
# particles, exclusives, etc., in the answer?

def regex_by_majority_response(regex):
    """
    Relates matches for the regular expression regex in the answer to
    majority response categories.
    """
    d = defaultdict(lambda : defaultdict(int))
    iqap = IqapReader('iqap-data.csv')
    for item in iqap.dev_set():
        # Regex search:
        match = False
        if regex.search(item.Answer):
            match = True
        # Majority label:
        maj_label = item.majority_label()
        d[maj_label][match] += 1
    # Print (category, percentage-match) pairs:
    print('Category', 'Percentage-matching')
    for label, match_dict in list(d.items()):
        print(label, match_dict[True] / float(sum(match_dict.values())))
        
# regex = re.compile(r'\b(thinks?|think|thought|can|could|shall|should|will|would|may|might|must)\b')
# regex_by_majority_response(regex)


#---------------------------------------------------------------------
# Question: Is 'definite-yes' more likely if the question and answer
# are syntactically similar?

def lexical_overlap(item):
    """
    Compare the lexical items in the question and answer to determine
    their degree of overlap. The score is the cardinality of the
    intersection divided by the cardinality of the union.
    """
    que_words = set(item.question_words(wn_lemmatize=True))
    ans_words = set(item.answer_words(wn_lemmatize=True))
    int_card = len(que_words & ans_words)
    union_card = len(que_words | ans_words)
    return int_card / float(union_card)

def lexical_overlap_by_definite():
    """
    Creates a CSV file named 'iqap-lexical-overlap-by-definite.csv'
    with the format

    Definite, LexicalOverlap

    where Definite is the number of 'definite' annotations for the
    item and LexicalOverlap is the question-answer intersection
    divided by the question-answer union, as given by
    lexical_overlap().
    """
    pairs = []
    iqap = IqapReader('iqap-data.csv')
    for item in iqap.dev_set():
        definite = item.definite_yes + item.definite_no
        pairs.append((definite, lexical_overlap(item)))
    csvwriter = csv.writer(open('iqap-lexical-overlap-by-definite.csv', 'w'))
    csvwriter.writerow(['Definite', 'LexicalOverlap'])
    csvwriter.writerows(pairs)
    
# lexical_overlap_by_definite()


    
                
    
    

