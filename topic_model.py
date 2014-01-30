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

import logging,sys
import re

from gensim import corpora, models, similarities
from utils import *

def filter_references(tokens):
  toks = [token for token in tokens if not re.match(r'\[\d{1,2}\]',token)]
  return toks

def clean_non_word_chars(tokens):
  toks = [re.sub(r'\W', "", token) for token in tokens]
  return toks

def main(argv):
  texts = [[ word for word in line.lower().split() if word not in english_stopwords] for line in open(argv[1])]
  all_tokens = sum(texts, [])
  filtered_tokens = filter(None,clean_non_word_chars(filter_references(all_tokens)))

if __name__ == '__main__': sys.exit(main(sys.argv))
