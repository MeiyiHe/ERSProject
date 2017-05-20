#!/usr/bin/env python
# File Name: compareTxtFiles.py
# Author: Meiyi (Lexi) He
# Description: A program that compares two text files line by line for similarity, 
#							 then output each lines' similarity in a new file as user indicates.
# To Compile & Run : python compareTxtFiles.py [OUTPUTFILE]
# output: a new file contains each lines' similarity between two files
# using difflib, SequenceMatcher

from sys import argv
import os
from difflib import SequenceMatcher

# define the method similar
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# reminds the user the output file
script, filename = argv
#print "We're going to write on %r." % filename

# open the file to write
target = open(filename, 'w')

# ask user to input 2 file name that they wanted to compare
fname1 = raw_input("Text Scripts to be compared : ")
fname2 = raw_input("SR Scripts to be compared : ")

# open those files 
f1 = open(fname1)
f2 = open(fname2)

# Reminds the user of the output file name
print "The output will be in %r." % filename 



# Read the first line from the files
f1_line = f1.readline()
f2_line = f2.readline()

# Initialize counter for line number
line_no = 1

# Loop if either file1 or file2 has not reached EOF
while f1_line != '' or f2_line != '':

	target.write( str( similar(f1_line, f2_line) ))
	# write a new line here to avoid overwriting previous similar precentage
	target.write('\n')
	# keep reading next lines
	f1_line = f1.readline()
	f2_line = f2.readline()

# close the output file once finished
target.close()


