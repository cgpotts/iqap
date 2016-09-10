# LSA 2011: Indirect question-answer pairs

Code and data for the Indirect Question-Answer Pairs (IQAP) corpus used in the
LSA 2011 course [Computational Pragmatics](http://compprag.christopherpotts.net/).


## File inventory

* `iqap-data.csv`: The corpus.

* `iqap.py`: module for working with `iqap-data.csv`

* `iqap_functions.py`: some examples of how to use `iqap.py` to work with the corpus.

This version is compatible with Python 2 and Python 3.


## Basic usage

```python
from iqap import IqapReader

corpus = IqapReader('iqap-data.csv')

for item in corpus.dev_set()[ : 2]:
    print(item.question_pos())
    print(item.answer_pos())

[('Did', 'VBD'), ('he', 'PRP'), ('do', 'VB'), ('a', 'DT'), \
 ('good', 'JJ-CONTRAST'), ('job', 'NN'), ('?', '.')]
[('He', 'PRP'), ('did', 'VBD'), ('a', 'DT'), ('great', 'JJ-CONTRAST'), \
 ('job', 'NN'), ('.', '.')]
[('Do', 'VBP'), ('you', 'PRP'), ('think', 'VB'), ('that', 'DT'),\
 ("'s", 'VBZ'), ('a', 'DT'), ('good', 'JJ-CONTRAST'),\
 ('idea', 'NN'), ('?', '.')]
[('It', 'PRP'), ("'s", 'VBZ'), ('a', 'DT'), ('terrible', 'JJ-CONTRAST'),\
 ('idea', 'NN'), ('.', '.')]
 ```

I hand-annotated the questions and answers for something approximating
the 'contrast' predicate. For example, in the simple dialogue "Was the
movie good? It was great.", the words _good_ and _great_ would be
highlighted. These annotations take the form of one or more nodes
suffixed with __-CONTRAST__. The Python classes include functionality
for grabbing these subtrees and working with their leaf nodes. The
`iqap.IqapReader` method `view_contrast_preds` gives you a sense for
what kind of information is available here. Here's a sample of the
output:

```python
corpus.view_contrast_preds()
======================================================================
Did he do a good job?
[Tree('JJ-CONTRAST', ['good'])]
He did a great job.
[Tree('JJ-CONTRAST', ['great'])]
======================================================================
Do you think that's a good idea?
[Tree('JJ-CONTRAST', ['good'])]
It's a terrible idea.
[Tree('JJ-CONTRAST', ['terrible'])]
======================================================================
...
```

For much more information: [http://compprag.christopherpotts.net/iqap.html](http://compprag.christopherpotts.net/iqap.html)




