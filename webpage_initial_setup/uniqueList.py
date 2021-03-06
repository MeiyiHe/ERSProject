#!/usr/bin/python
import sys
import os
import string
import functools
import operator
import re
import time
from collections import defaultdict
import linecache



def uniqueList(file, dirname):

	num = 0
	# define punctuations, read file and take off all punctuations
	punctuations = set('''!()-[]{};:'"\,<>./?@#$%^&*_~\n''')
	with open(file) as infile:
		c = infile.read()

		line = c.split()
		num += len(line)
		words = set(line)

	# make all words to lower, and build a set
	words = [''.join(c for c in s if c not in punctuations) for s in words]
	words = [x.lower() for x in words]
	unique = set()
	
	# initialize the 'Library' file
	libPath = dirname + '/Library.txt'
	initLib = open(libPath, 'w')
	

	# write all unique words in Library
	for w in words:
		if w not in unique:
			unique.add(w)
			initLib.write(w)
			initLib.write('\n')

	initLib.close()

	# count unique words
	uniqueWords = defaultdict(int)
	for element in unique:
		uniqueWords[element] += 1

	return uniqueWords



def setCover(file, dirname):
	
	# since first time user, create a directory to store things
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	sentenceNumArray = []
	coverageArray = []
	listWithFrq = defaultdict(int)
	listWithLine = defaultdict(dict)
	punctuations = set('''!()-[]{};:'"\,<>./?@#$%^&*_~\n''')
	
	# process talk notes for later USER script generating
	dest1 = open('scriptsTN.txt','w')
	with open(file) as infile:
		new = infile.read()
		for line in new.split('. '):
			dest1.write(line)

			dest1.write('\n')
	dest1.close()
	
	dest2 = open('userScripts.txt','w')
	with open('scriptsTN.txt') as infile:
		for line in infile:
			if not line.isspace():
				dest2.write(line)

	dest2.close()
	#os.remove('scriptsTN.txt')

	# process talk notes for unique sentence prompting
	dest3 = open('processLower.txt','w')
	with open(file) as infile:
		new = infile.read()
		for line in new.split('. '):
			dest3.write(line.lower())
			dest3.write('\n')
	dest3.close()

	dest4 = open('lowerScript.txt','w')
	with open('processLower.txt') as infile:
		for line in infile:
			if not line.isspace():
				dest4.write(line)
	dest4.close()
	os.remove('processLower.txt')
	
	# build hashmaps from the lowerScripts.txt
	with open('lowerScript.txt') as infile:
		for i, line in enumerate(infile):
			for word in line.split(' '):
				string = ''.join(c for c in word if c not in punctuations)
				listWithFrq[string] += 1
				listWithLine[i][string] = listWithFrq[string] 

	# get the unique word list
	listUnique = uniqueList(file, dirname)

	total = len(listUnique)
	
	#find a sentence that contains most less frequncy words from listWithLine
	frqCount = 0
	listTemp = defaultdict(int)
	search = 1
	count = 999999
	countResult = 0
	timesOfReduce = 0
	total = len(listUnique)
	counter = 0
	scCount = 1
	writeUniqueList = 0

	userPath = dirname + '/scriptsRequest.txt'
	print userPath
	scripts = open( userPath ,'w')
	#scripts = open('scriptsRequest.txt','w')
	systemPath = dirname + '/scriptsSystem.txt'
	print systemPath
	scriptsSystem = open( systemPath ,'w')
	#scriptsSystem = open('scriptsSystem.txt','w')

	
	# while unique list is not empty
	while bool(listUnique):
		
		c = 0
		if bool(listTemp):
			frqCount = 0
			line = 0

		# checking each lines, find the line that contains most unique words
		for k,v in listWithLine.items():
			count1 = 0

			for a,b in v.items():
				if a in listUnique.keys():
					count1 += 1
				if frqCount < count1:
					frqCount = count1
					listTemp.clear()
					line = k
		# store the line in temp
		temp = listWithLine[line]

		for key, val in temp.items():
			listTemp[key] = val

		prev = counter

		# calculating rate 
		rate = float(counter)/float(total)
		# only when less than 75%, write sentences
		if rate <= 0.75:
			#print rate
			scripts.write("SENTENCE ( " + str(scCount) + " ): \n")
			scCount += 1

			# write the lines to script and pop out from unique list
			scripts.write(linecache.getline('userScripts.txt', line+1) +"\n")
			scriptsSystem.write(linecache.getline('lowerScript.txt', line+1) +"\n")
			for k, v in listWithLine.pop(line).items():
				if k in listUnique.keys():
					listUnique.pop(k)
					counter += 1

			listTemp.clear()


		if count > len(listUnique):
			count = len(listUnique)
			timesOfReduce += 1

		# when less than 25%, write words
		if rate > 0.75 and rate < 1:

			if writeUniqueList == 0:
				tmp = []
				#print listUnique
				for k,v in listUnique.iteritems():
					tmp.append(str(k))
					#print k
				ten_words = []
				total = []
				for i in range(len(tmp)):
					if len(ten_words) <= 10:
						ten_words.append(tmp[i])
						print tmp[i]
					else:		
						#print "empty"				
						total.append(ten_words)
						#print ten_words
						ten_words = []
				if len(ten_words) != 0:
					#print ten_words
					total.append(ten_words)

				for i in range(len(total)):
					scripts.write("WORD LIST ( " + str(i+1) + " ): \n")
					for j in range(len(total[i])):
						scripts.write(total[i][j])
						scriptsSystem.write(total[i][j])
						scripts.write(' ')
						scriptsSystem.write(' ')
					scripts.write('.\n')

				listUnique.clear()
				

			writeUniqueList = 1
							

		line = 0
		frqCount = 0

		#print total
		sentenceNumArray.append(timesOfReduce)
		coverageArray.append(rate*100)


	scripts.close()
	scriptsSystem.close()


	return 



#unique = uniqueList('abkTalkNote.txt')
#setCover('0530-note/7sen.txt')
#setCover('/Users/meiyihe/Desktop/testUploadFile/0530-note/11sen.txt', 'meiyiFolder')
#setCover('/Users/meiyihe/Desktop/testUploadFile/super.txt','meiyiFolder')
#uniqueList('/Users/meiyihe/Desktop/testUploadFile/0530-note/11sen.txt','meiyiFolder')
#setCover('/Users/meiyihe/Desktop/testUploadFile/0530-note/11sen.txt','meiyiFolder')








