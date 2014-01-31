#!/usr/bin/env python
"""Copyright (C) 2014 Romain Deveaud <romain.deveaud@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import logging,sys
import re

from gensim import corpora, models, similarities
from utils import *

def filter_references(tokens):
  """
  Removes references from the text.
  Handles ACM style references (e.g. [22]).
  """
  toks = [token for token in tokens if not re.match(r'\[\d{1,2}\]',token)]
  return toks

def clean_non_word_chars(tokens):
  """
  Cleans a list of words from non-word characters.
  """
  toks = []
  for token in tokens:
    t = re.sub(r'\W', "", token)
    if len(t) > 1:
      toks.append(t)

  return toks

def train_lda(texts):
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  print "Building gensim corpus..."
  dictionary = corpora.Dictionary(texts)
  corpus = [dictionary.doc2bow(text) for text in texts]
  print "Done."
  model = models.LdaModel(id2word=dictionary, num_topics=13,passes=20,update_every=0)
  model.VAR_MAXITER = 500
  model.VAR_THRESH  = 0.0001
  model.update(corpus)

  model.print_topics(13)

def proceedings2text(conf,year):
  path = get_conf_path(conf,year)+'/txt'
  text_proceedings = []

  print "Formatting corpus..."
  for root, subFolders, files in os.walk(path):
    for f in files:
      texts = [[ word for word in line.lower().split() if word not in english_stopwords] for line in open(os.path.join(root,f))]
      all_tokens = sum(texts, [])
      filtered_tokens = filter(None,clean_non_word_chars(filter_references(all_tokens)))
      text_proceedings.append(filtered_tokens)

  print "Done."
  return text_proceedings

def main(argv):
  train_lda(proceedings2text(argv[1],argv[2]))

if __name__ == '__main__': sys.exit(main(sys.argv))
