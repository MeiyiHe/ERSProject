#!/usr/bin/env python
# File Name: convertAlltoUpper.py
# Author: Meiyi (Lexi) He
# Description: A program that convert all texts to upper case in a txt file
# To Compile & Run : python convertAlltoUpper.py 
# output: 
import os

filename = raw_input("File that you want to convert all upper: ") 

if filename and os.path.isfile(filename):
  with open(filename, 'r') as f:
      txt = f.read()
  newfp = '{0}_upper{1}'.format(*os.path.splitext(filename))
  with open(newfp, 'w') as f:
      f.write(txt.upper())

f.close()

