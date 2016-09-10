#!/usr/bin/env python

"""
Functionality for using the iqap-data.csv corpus.

IqapReader is the central interface. The action is in Item objects,
which model the row values and provide some methods for dealing with
them (especially useful for the trees).

The main method prints a basic view of the items to standard output.
"""

__author__ = "Christopher Potts"
__credits__ = []
__version__ = "2.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

import csv
from operator import itemgetter
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer

######################################################################

class IqapReader:
    """
    Class for dealing with the entire corpus. Can intuitively
    be thought of as a collection of Item objects with some
    additional structure and grouping.
    """
    
    def __init__(self, src_filename):
        """Instances are build from the full-path filename for iqap-data.csv."""
        self.src_filename = src_filename

    def iter_items(self):
        """Iterate through all the items. Rarely used because it exposes the evaluation set."""
        with open(self.src_filename, 'rt') as f:
            csvreader = csv.reader(f)
            header = next(csvreader)
            for row in csvreader:
                yield Item(row, header)

    def dev_set(self):
        """Returns the list of development items."""
        dev = []
        for item in self.iter_items():
            if item.DevEval == "DEVELOPMENT":
                dev.append(item)
        return dev

    def eval_set(self):
        """Returns the list of evaluation items."""
        e = []
        for item in self.iter_items():
            if item.DevEval == "EVALUATION":
                e.append(item)
        return e

    def item_by_id(self, item_id):
        """Get an item based on its Id, i.e., the value for the Item attribute Item.
        Raises an exception of the Id isn't in the data."""
        for item in self.iter_items():
            if item.Item == item_id:
                return item
        raise ArgumentException("The Id %s is not present in the data" % item_id)
        
    def view_contrast_preds(self):
        """Look at how the contrast pred annotations work in the
        development set, via printing to standard output."""    
        for item in self.dev_set():
            print("======================================================================")
            print(item.Question)
            print(item.question_contrast_pred_trees())
            print(item.Answer)
            print(item.answer_contrast_pred_trees())

######################################################################
    
class Item:
    """
    Class for computing the rows in iqap-data.csv --- the items in all
    their glory.  The assumption is that these will be built as part
    of instantiating an IqapCorpus, though they would be build from
    the list correspondong to the header in iqap-data.csv and the list
    corresponding to the row of interest.
    """
    
    def __init__(self, row, header):
        """
        Arguments:

        row (list) -- the items corresponding to a row in iqap-data.csv
        header (lit) --- the first row of iqap-data.csv

        The initialization method maps each row value to an
        attiribute named by the corresponding header value. Thus,
        we have the following attributes with associted types:

	Item (int) -- Item number
        Classification (str) -- CNN, Yahoo, Hirschberg
        Source	(str) -- Source file where applicable, else repeats Classification
        Question (str) -- question text
        Answer (str) -- answer text
        Prefix (str) -- 'yes', 'no' or blank
        definite-yes (int) -- number of annotators who chose this category (0..30)
        probable-yes (int) -- number of annotators who chose this category (0..30)
        definite-no (int) -- number of annotators who chose this category (0..30)
        probable-no (int) -- number of annotators who chose this category (0..30)
        DevEval	(str) -- DEVELOPMENT or EVALUATION
        QuestionParse (nltk.tree.Tree) -- Stanford parser parse, with hand corrections, of Question
        AnswerParse (nltk.tree.Tree) -- Stanford parser parse, with hand corrections, of Answer
        """        
        for i in range(len(header)):
            att_name = header[i].replace('-', '_')
            att_val = row[i]
            if att_name in ('definite_yes', 'probable_yes', 'definite_no', 'probable_no', 'Item'):
               att_val = int(att_val)
            elif att_name in ('QuestionParse', 'AnswerParse'):
               att_val = Tree.fromstring(att_val)
            setattr(self, att_name, att_val)

    def response_counts(self, make_binary=False):
        """
        Dictionary mapping response category names to counts:

        { 'definite_yes': self.definite_yes,
          'probable_yes': self.probable_yes,
          'definite_no': self.definite_no,
          'probable_no': self.probable_no }

        Option make_binary=True returns:

        { 'yes': self.definite_yes+self.probable_yes,
          'no':self.definite_no+self.probable_no }
        """        
        if make_binary:
            return {
                'yes': self.definite_yes+self.probable_yes,
                'no':self.definite_no+self.probable_no
                }
        else:        
            return {'definite_yes': self.definite_yes,
                    'probable_yes': self.probable_yes,
                    'definite_no': self.definite_no,
                    'probable_no': self.probable_no}
        
    def response_dist(self, make_binary=False):
        """
        Turn self.response_counts() into a probability distribution,
        with the same keys.
        """        
        p = {}
        counts = self.response_counts(make_binary=make_binary)
        total = float(sum(counts.values()))
        for key, val in list(counts.items()):
            p[key] = val / total
        return p

    def majority_label(self):
        """Return the label with at least 15 responses, if there is one, else return None."""
        max_label, max_count = sorted(list(self.response_counts().items()), key=itemgetter(1), reverse=True)[0]
        if max_count <= 15:
            max_label = None
        return max_label

    def max_label(self, make_binary=False):
        """
        Return the label with the largest number of counts.  If this
        is not unique (if two or more categories are tied), return
        None.
        """        
        sorted_dict = sorted(list(self.response_counts(make_binary=make_binary).items()), key=itemgetter(1), reverse=True)
        # If there is a tie for max label, then there is no max label.
        label, count = sorted_dict[0]
        if count == sorted_dict[1][1]:
            return None
        else:
            return label

    def question_pos(self, wn_lemmatize=False):
        """Return the (string, pos) pairs for the question. wn_lemmatize=True
        runs them through the WordNet lemmatizer."""
        pos = self.QuestionParse.pos()
        if wn_lemmatize:
            pos = list(map(self.wn_lemmatize, pos))
        return pos

    def question_words(self, wn_lemmatize=False):
        """Return the words of the question parse. wn_lemmatize=True
        runs them through the WordNet lemmatizer using their POS tags
        (which are removed)."""
        pos = self.question_pos(wn_lemmatize=wn_lemmatize)
        return [lem[0] for lem in pos]

    def answer_pos(self, wn_lemmatize=False):
        """Return the (string, pos) pairs for the answer. wn_lemmatize=True
        runs them through the WordNet lemmatizer."""
        pos = self.AnswerParse.pos()
        if wn_lemmatize:
            pos = list(map(self.wn_lemmatize, pos))
        return pos

    def answer_words(self, wn_lemmatize=False):
        """Return the words of the answer parse. wn_lemmatize=True
        runs them through the WordNet lemmatizer using their POS tags
        (which are removed)."""
        pos = self.answer_pos(wn_lemmatize=wn_lemmatize)
        return [lem[0] for lem in pos]
        
    def question_contrast_pred_trees(self):
        """Returns the list of -CONTRAST-rooted trees in the question."""
        return self.contrast_pred_trees(self.QuestionParse)

    def question_contrast_pred_pos(self):
        """Returns the list of (word, pos) pairs derived fom the leaves in the -CONTRAST-rooted trees in the question."""
        trees = self.question_contrast_pred_trees()
        return self.contrast_tree_pos(trees)
    
    def answer_contrast_pred_trees(self):
        """Returns the list of -CONTRAST-rooted trees in the answer."""
        return self.contrast_pred_trees(self.AnswerParse)  

    def answer_contrast_pred_pos(self):
        """Returns the list of (word, pos) pairs derived fom the leaves in the -CONTRAST-rooted trees in the question."""
        trees = self.answer_contrast_pred_trees()
        return self.contrast_tree_pos(trees)

    def contrast_tree_pos(self, trees):
        """For the given set of nltk.tree.Tree objects trees, returns the list of (word, pos) pairs associated with the leaves.
        Primarily for use by self.question_contrast_pred_pos() and self.answer_contrast_pred_pos()."""
        lems = []
        for tree in trees:
            lems += list(map(self.wn_lemmatize, tree.pos()))
        return lems

    def contrast_pred_trees(self, tree):
        """For the nltk.tree.Tree objects tree, returns the list of -CONTRAST-rooted subtrees.
        Primarily for use by self.question_contrast_pred_trees() and answer_contrast_pred_trees()."""
        trees = []
        for subtree in tree.subtrees():
            if subtree.label().endswith("-CONTRAST"):
                trees.append(subtree)
        return trees

    def wn_lemmatize(self, lemma):
        """
        Lemmatize the supplied (word, pos) pair using
        nltk.stem.WordNetLemmatizer. If the tag corresponds to a
        WordNet tag, then we convert to that one and use it, else we
        just use the strong for lemmatizing.
        """        
        string, tag = lemma
        string = string.lower()
        tag = tag.lower()
        wnl = WordNetLemmatizer()
        if tag.startswith('v'):    tag = 'v'
        elif tag.startswith('n'):  tag = 'n'
        elif tag.startswith('j'):  tag = 'a'
        elif tag.startswith('rb'): tag = 'r'
        if tag in ('a', 'n', 'r', 'v'):        
            return (wnl.lemmatize(string, tag), tag)
        else:
            return (wnl.lemmatize(string), tag)  

######################################################################

if __name__ == '__main__':
    """If the main method is called, print a basic form of the data to standard output."""
    corpus = IqapReader('iqap-data.csv')
    for item in corpus.dev_set():
        print("======================================================================")
        print(item.Question)
        print(item.Answer)
        print(sorted(item.response_dist()))
        
