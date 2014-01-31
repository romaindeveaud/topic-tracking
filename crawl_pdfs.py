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

import sys
import re
import urllib2
import hashlib
from bs4 import BeautifulSoup
from utils import *


def get_acm_doi_links_from_dblp(conf,year):
  """
  Given the acronym of a conference and a year, this method extracts 
  the ACM DOI links of the papers from DBLP.

  TODO: it could consider many other repositories by changing the
        regex.
  """

  dblp_url = 'http://www.informatik.uni-trier.de/~ley/db/conf/'+ \
              conf+'/'+conf+year+'.html'

  dblp_parsed_html = BeautifulSoup(urllib2.urlopen(dblp_url).read())

  acm_links = dblp_parsed_html.body.findAll('a',attrs={'href':re.compile('doi\.acm\.org')})
  return [link['href'] for link in acm_links]

def get_pdf_from_acm_url(url):
  """
  It requires an access to the ACM DL library.
  Creates the appropriate folder if it does not exist, then download the
  PDF of the paper corresponding to the DOI link given as argument.
  """
  
  acm_parsed_html = BeautifulSoup( \
                      urllib2.urlopen( \
                        urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) \
                      ).read() \
                    )
  pdf_link = 'http://dl.acm.org/'+acm_parsed_html.body.find('a',attrs={'name':'FullTextPDF'})['href']

  pdf = urllib2.urlopen(urllib2.Request(pdf_link, headers={'User-Agent' : "Magic Browser"})).read()
  return pdf

def download_pdf(pdf_data,destination):
  """
  Write the PDF data at the specified destination.
  """
  pdf_file = open(destination,'wb')
  pdf_file.write(pdf_data)
  pdf_file.close()

def main(argv):
  for link in get_acm_doi_links_from_dblp(argv[1],argv[2]):
    download_pdf(get_pdf_from_acm_url(link),pdf_path+'/'+(abs(hash(link)) % (10 ** 8))+'.pdf')


# TODO: check the arguments, maybe with an option parser.
if __name__ == '__main__': sys.exit(main(sys.argv))
