#!/usr/bin/env python
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
