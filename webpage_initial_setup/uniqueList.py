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

	
	return uniqueWords

def setCover(file, dirname):
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
	#print listUnique
	#print "in setcover method(): length of listUnique: ", len(listUnique)
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
			#print(linecache.getline('userScripts.txt', line+1) +"\n")
			#print listUnique
			#print listTemp
			scripts.write(linecache.getline('userScripts.txt', line+1) +"\n")
			scriptsSystem.write(linecache.getline('lowerScript.txt', line+1) +"\n")
			for k, v in listWithLine.pop(line).items():
				if k in listUnique.keys():
					listUnique.pop(k)
					counter += 1

			listTemp.clear()
			#print listUnique

		#print "after checking rate : ", rate

		if count > len(listUnique):
			#print "count: " + str(count) + " length of listUnique: " + str(len(listWithLine))
			count = len(listUnique)
			timesOfReduce += 1


		if rate > 0.75 and rate < 1:
			#print "in > 0.85"
		#if len(listUnique) != 0 and len(listTemp) == 0:
			if writeUniqueList == 0:
				tmp = []
				#print listUnique
				for k,v in listUnique.iteritems():
					tmp.append(str(k))
				ten_words = []
				total = []
				for i in range(len(tmp)):
					if len(ten_words) < 10:
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



#unique = uniqueList('abkTalkNote.txt')
#setCover('0530-note/7sen.txt')
#setCover('/Users/meiyihe/Desktop/testUploadFile/0530-note/5sen.txt', 'meiyiFolder')








