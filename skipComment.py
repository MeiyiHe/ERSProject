#!/usr/bin/env python
# File Name: .py
# Author: Meiyi (Lexi) He
# Description: A program that convert all texts to upper case in a txt file
# To Compile & Run : python convertAlltoUpper.py 
# output: 
# normalize text input 
# 1) all to upper cases
# 2) take out punctuations

import os
import re


filename = raw_input("File that you want to convert all upper: ") 

if filename and os.path.isfile(filename):
  with open(filename, 'r') as f:
  	newfp = '{0}_upper{1}'.format(*os.path.splitext(filename))
  	with open(newfp, 'w') as f1:
  		
  		for line in f:
  			line.strip().split() 
  			if line.startswith('//'):
  				pass
  			else:
  				f1.write(line.upper().strip())
f.close()

