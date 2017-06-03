#!/usr/bin/python
import checker
from collections import defaultdict
import sys
import os
import string
import functools
import operator
import re
import time
import linecache

def newUniqueList( newfile, dirname ):	

	userLib = '/Library.txt'
	# get the word set that need to add to library
	libPath = dirname + userLib
	toAdd = checker.newWordSet(newfile, libPath)
	
	
	lib = open(libPath, 'a')
	for w in toAdd:
		lib.write(w)
		lib.write('\n')
	lib.close()
	#print toAdd
	uniqueWords = defaultdict(int)
	for w in toAdd:
		uniqueWords[w] += 1
	print uniqueWords
	return uniqueWords



def returnUserSetCover(file, dirname):
	#directory = os.path.dirname(name)
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
	#listUnique = uniqueList(file)
	listUnique = newUniqueList( file , dirname)

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
	

	#count

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

		prev = counter


		rate = float(counter)/float(total)
		if rate <= 0.75:
			#print rate
			scripts.write("SENTENCE ( " + str(scCount) + " ): \n")
			scCount += 1

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


		if rate > 0.75 and rate < 1:
			
			if writeUniqueList == 0:
				tmp = []
				#print listUnique
				for k,v in listUnique.iteritems():
					tmp.append(str(k))
				ten_words = []
				total = []
				for i in range(len(tmp)):
					if len(ten_words) <= 10:
						ten_words.append(tmp[i])
					else:		
						#print "empty"				
						total.append(ten_words)
						ten_words = []
				if len(ten_words) != 0:
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




#newUniqueList('0530-note/addNewLib.txt','Library.txt', 'meiyiFolder')
#returnUserSetCover('0530-note/addNewLib.txt', 'meiyiFolder' )















