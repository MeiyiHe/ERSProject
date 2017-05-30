#uniqueList('file')
import sys
import os
import string
import functools
import operator
import re
import time
from collections import defaultdict
import linecache
import matplotlib.pyplot as plt
import seaborn as sns



def uniqueList(file):

	num = 0
	punctuations = set('''!()-[]{};:'"\,<>./?@#$%^&*_~\n''')
	with open(file) as infile:
		c = infile.read()

		line = c.split()
		num += len(line)
		words = set(line)

	#print uniqueWords
	words = [''.join(c for c in s if c not in punctuations) for s in words]
	words = [x.lower() for x in words]
	unique = set()
	for w in words:
		if w not in unique:
			unique.add(w)

	uniqueWords = defaultdict(int)
	for element in unique:
		uniqueWords[element] += 1
	#print uniqueWords
	print "Original File have (words count): ", num
	print "Current Words Count: ", len(words)
	print "Current Unique Words Count: ", len(uniqueWords)
	
	return uniqueWords

def setCover(file):
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
			#print "in function"
			dest1.write(line)
			#dest1.write('.')
			dest1.write('\n')
	dest1.close()

	dest2 = open('userScripts.txt','w')
	with open('scriptsTN.txt') as infile:
		for line in infile:
			if not line.isspace():
				dest2.write(line)

	dest2.close()
	os.remove('scriptsTN.txt')

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
	listUnique = uniqueList(file)
	print listUnique
	print "in setcover method(): length of listUnique: ", len(listUnique)
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
	scripts = open('scriptsRequest.txt','w')
	scriptsUnder = open('scriptsUnder.txt','w')
	#dest = open('coveringSentence.txt','w')
	while bool(listUnique):
		c = 0
		if bool(listTemp):
			frqCount = 0
			line = 0

		for k,v in listWithLine.items():
			count1 = 0

			for a,b in v.items():
				if a in listUnique.keys():
					count1 += 1
				if frqCount < count1:
					frqCount = count1
					listTemp.clear()
					line = k

		temp = listWithLine[line]

		for key, val in temp.items():
			listTemp[key] = val
		print('\n=========getline=============\n')

		prev = counter
		for k, v in listWithLine.pop(line).items():
			if k in listUnique.keys():
				listUnique.pop(k)
				counter += 1

		rate = float(counter)/float(total)
		if rate < 0.75:
			print rate
			scripts.write("Sentence ( " + str(scCount) + " )\n")
			scCount += 1
			scripts.write(linecache.getline('userScripts.txt', line+1) +"\n")
			scriptsUnder.write(linecache.getline('lowerScript.txt', line+1) +"\n")

		line = 0
		frqCount = 0
		listTemp.clear()
		if count > len(listUnique):
			print "count: " + str(count) + " length of listUnique: " + str(len(listWithLine))
			count = len(listUnique)
			timesOfReduce += 1

		if rate >= 0.75:
			if writeUniqueList == 0:
				for k, v in listUnique.iteritems():
					print '%s' % (k)
					scripts.write('%s' % (k))
					scripts.write('\n')
				writeUniqueList = 1

		sentenceNumArray.append(timesOfReduce)
		coverageArray.append(rate*100)


	scripts.close()
	scriptsUnder.close()

	# plt.plot(sentenceNumArray, coverageArray)
	# plt.axis([0,countResult,0,100])
	# plt.xlabel('Number of Sentences')
	# plt.ylabel('Words Covered Rate (%)')
	# plt.show()
	return 













#unique = uniqueList('abkTalkNote.txt')
setCover('abkTalkNote.txt')








