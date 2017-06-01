#!/usr/bin/python

#	Usage: python textProcess.py txtfile_to_read.txt txtfile_to_write.txt txtfile_to_write_freq.txt
#	txtfile_to_read.txt is the file of the input script ("/.../input_script_170224_004.txt")


#	XXXXdeferedXXXXXtxtfile_to_write.txt is the file containing distinct words in the input script ("/.../output_words.txt")
#	XXXXdeferedXXXXXtxtfile_to_write_freq.txt is the file containing respective frequencies of words in txtfile_to_write ("/.../output_freq.txt")

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
	#print len(tokens)	


def output_script(string_to_read, file_to_write):
	
	#analyzer("/Users/Siya/Desktop/ERSPGroup/PROCESSED_170224_003_SAMPLE.txt")
	#file_to_read = sys.argv[1]
	#####file_to_write = sys.argv[2]
	#####file_to_write_freq = sys.argv[3]
	#####buf = open(file_to_write,"w")
	#####buf_freq = open(file_to_write_freq, "w")


	
	wr = open(file_to_write, 'w')

	tokens = [e.upper() for e in map(string.strip, re.split("(\W+)",string_to_read)) if len(e) > 0 and not re.match("\W", e)]

	for i in range(len(tokens)):
		print(tokens[i]),
		wr.write(tokens[i])
		wr.write(" ")	
"""
	no_lim = []
	buff = []

	punc = [',','.','?']
	
	for wd in string_to_read:
		if wd in punc or (ord(wd) <=90 and ord(wd) >=65) or (ord(wd) <=122 and ord(wd) >=97):
			buff.append(wd)
		else:
			if len(buff)!=0:
				no_lim.append(''.join(buff))
				buff = []

	analyzer(file_to_read)


	for i in range(len(tokens)):
		print(tokens[i].upper()),
		wr.write(tokens[i].upper())
		wr.write(" ")"""
		#print(tokens[i]),
		#print(no_lim[i])


		######buf.write(b[i])
		######buf.write(" ")
		######buf_freq.write(str(occ[i]))
		######buf_freq.write(" ")
	
		

	#test = []

	#test.append("design")
"""
	bufferChunk = []
	buf = open(file_to_write,"w")

	for i in range(len(tokens) - 1):
		if(tokens[i] not in test):
			bufferChunk.append(tokens[i])
			#print bufferChunk
			#print("\n")
		else:
			#bufferChunk.write()
			print bufferChunk
			for j in range(len(bufferChunk)):
				buf.write(bufferChunk[j])
				buf.write(" ")

			print("\n\n\n")
			del bufferChunk[:]

	print bufferChunk
	for j in range(len(bufferChunk)):
		buf.write(bufferChunk[j])
		buf.write(" ")


	print "\n\n"
"""
