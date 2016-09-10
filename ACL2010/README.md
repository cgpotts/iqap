# Data and code for de Marneffe et al. 2010

## Reference

de Marneffe, Marie-Catherine, Christopher D. Manning and Christopher Potts. 2010. ["Was it good? It was provocative." Learning the meaning of scalar adjectives](http://aclweb.org/anthology/P/P10/P10-1018.pdf). In Proceedings of the 48th Annual Meeting of the Association for Computational Linguistics, 167-176. Uppsala, Sweden: Association for Computational Linguistics.

## Inventory

* `all-ngrams.txt`, `all-unigrams.txt`: inventory files used for inspection and gathering auxiliary stats

* `avoided-adjective.txt`: special cases where the reply drops an adjective (Q: 'Is it a huge gap?' A: 'It's a gap')

* `data`: data files.
  * Unzip `imdb-reviewfield.unigrams-5threshold.csv` before use.
  * `imdb-reviewfield.ngrams.csv` and `imdb-reviewfield.unigrams-5threshold.csv` have the same format.
  * `expensive-college.csv`, `land.csv`, and `young_kids.csv` contain stats derived from Web searches, to be used to fit logistic regression models.

* `dicts.py`: pre-`collections` dicts with default values

* `experiments.py` and `scalars.py`: core experiment code.

* `indirect-answers.combined.imdb-predictions.csv`: predictions, the output of `experiments.py`. To get to the final tables in the paper, one still has to cobble together a few stats derived from other data files by hand, unfortunately.

* `mturk-indirect-answers.combined.csv`: annotation results

* `mturk-setup`: contains the files for the annotation project

* `wn`: our sentiment lexicon, as described in the paper.
  




