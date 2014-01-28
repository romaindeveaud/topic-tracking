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


"""
This script recursively retrieves all the PDFs stored in papers/<conf>/pdf/ and
extract their text using the pdf2txt.py utility.
Extracted text is stored in papers/<conf>/txt/.  
"""

# TODO: only extract the text of papers that we haven't seen so far.

import sys
import os
import subprocess


def main(argv):
  rootdir = os.getcwd()+'/papers'

  for root, subFolders, files in os.walk(rootdir):
    for f in files:
      fileName, fileExtension = os.path.splitext(f) 
      if fileExtension == ".pdf":
        input_file = os.path.join(root,f)
        output_file = input_file.replace('pdf','txt')
        
        subprocess.call(["python","pdf2txt.py","-o",output_file,input_file])

if __name__ == '__main__': sys.exit(main(sys.argv))
