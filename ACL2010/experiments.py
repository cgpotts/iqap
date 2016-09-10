#!/usr/bin/env python

import re
import csv
import numpy
from dicts import DefaultDict
from operator import itemgetter
from scalars import Dictionary, Evaluator

def assess_imdb():
    predictions_filename = "indirect-answers.combined.imdb-predictions.csv"
    dictionary_filenames = [
        "data/imdb-reviewfield.unigrams-5threshold.csv",
        "data/imdb-reviewfield.ngrams.csv"]
    dialogues_filename = "mturk-indirect-answers.combined.csv"
    e = Evaluator(dictionary_filenames, dialogues_filename, predictions_filename)
    means_predictions = e.with_means()
    maxs_predictions = e.with_maxs()
    sentiment_predictions = e.with_wordnet()
    e.create_predictions_file([means_predictions, "means"], [sentiment_predictions, "sentiment"])

assess_imdb()
