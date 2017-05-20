#!/usr/bin/python
# File Name: textProcess
# Author: Meiyi (Lexi) He
# Description: TODO


import sys
import string, os
import re
import csv
import collections
import operator
from collections import Counter

#tokens = []

# This point is to modify the file and mapping out all the puncuations from file
def analyzer(ifile):
	global tokens

	file = open(ifile, "r")
	file = file.read();
	#This is to filter out puncuation in the text, should not worry about in input 
	tokens = [e.lower() for e in map(string.strip, re.split("(\W+)",file)) if len(e) > 0 and not re.match("\W", e)]

	#print tokens
	print len(tokens)			

if __name__ == "__main__":
	#print "Input file path:"
	#ifile = raw_input("Which file you want to process? ");
	analyzer("txt1.txt")

	print "\n\n"
	dictionary = {}
	freq = Counter(tokens)
	# counter will return a list  (words, freq) {'test': 10, 'is': 2, ...}
	for i in range (len(tokens)):
		dictionary[tokens[i]] = freq[tokens[i]]

	sorted_dict = sorted( dictionary.items(), key = lambda x: (-x[1], x[0]))

	print sorted_dict
	# sorted --> list of sorted tuples based on the frequency : [('text', 1), ('am', 1), ...]

	print "\n\n"

