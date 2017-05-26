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

#store sentence into dict of dict 
listWithFrq = defaultdict(int)
listWithLine = defaultdict(dict)
punctuations = set('''!()-[]{};:'"\,<>./?@#$%^&*_~\n''')


sentenceNumArray = []
coverageArray = []

# split abkTalkNote into sentences, delimiter as "." --> period
dest = open('abkTN.txt','w')
with open('abkTalkNote.txt') as infile:
	tNew = infile.read()
	for line in tNew.split('. '):
		dest.write(line)
		dest.write('\n')
dest.close()

destUnder = open('abkTNUnder.txt','w')
with open('abkTalkNote.txt') as infile:
	tNew = infile.read()
	for line in tNew.split('. '):
		destUnder.write(line.lower())
		# add destUnder for writing scripts just for our own usage
		destUnder.write('\n')
destUnder.close()		


# clearing the space within abkTN.txt
newDest = open('abkTNew.txt','w')
with open('abkTN.txt','r') as file:
    for line in file:
        if not line.isspace():
            newDest.write(line)
newDest.close()

# clearing the space within abkTN.txt
newDestUnder = open('abkTNewUnder.txt','w')
with open('abkTNUnder.txt','r') as file:
    for line in file:
        if not line.isspace():
            newDestUnder.write(line)
newDestUnder.close()


# build hashmaps 
with open('abkTNewUnder.txt') as infile:
	for i, line in enumerate(infile):	
		for word in line.split(' '):
			string = ''.join(c for c in word if c not in punctuations)
			listWithFrq[string] += 1
			listWithLine[i][string] = listWithFrq[string] 


#unique words in dict 
listUnique = defaultdict(int)  
with open('TNnotDuplicate.txt') as infile:
	c = infile.read()
	for word in c.split('\n'):
		listUnique[word] += 1

#find a sentence that contains most less frequncy words from listWithLine
frqCount = 0
listTemp = defaultdict(int)
search = 1
count = 999999
countResult = 0
timesOfReduce = 0


with open('abkTNewUnder.txt') as infile:
	c = infile.read()
	for word in c.split('\n'):
		countResult += 1

print "total sentence number:"
print countResult

scripts = open('scriptsRequest.txt','w')
scriptsUnder = open('scriptsUnder.txt','w')
analysis = open('coverageAnalysis.txt','w')
dest1 = open('coveringSentence.txt','w')
#print listWithLine
total = len(listUnique)
counter = 0
scCount = 1
writeUniqueList = 0
while bool(listUnique):
	c = 0
	if bool(listTemp):
		# first = listWithLine.values()[0]
		frqCount = 0
		line = 0


	#check if list contain high frq and update
	for k,v in listWithLine.items():

		count1 = 0
		for a, b in v.items():
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
	dest1.write('\n')
	for k,v in listWithLine.pop(line).items():
		if k in listUnique.keys():
			listUnique.pop(k)
			counter += 1

	
	analysis.write("Covering " + str(counter-prev) + " more\n")
	analysis.write("Current lines cover " + str(counter) + " words\n")
	
	#print "covering " + str(counter) + " words"
	rate = float(counter)/float(total)
	# print "Rate of coverage: " + str(rate)
	analysis.write("Rate of coverage: " + str(rate) + "\n")
	analysis.write("Line Number from input file: " + str(line+1) +"\n")
	analysis.write(linecache.getline('abkTNew.txt', line+1))
	
	if rate < 0.75:
		scripts.write("Sentence ( " + str(scCount) + " )\n")
		scCount += 1
		scripts.write(linecache.getline('abkTNew.txt', line+1) +"\n")
		scriptsUnder.write(linecache.getline('abkTNewUnder.txt', line+1) +"\n")
	

	line = 0
	frqCount = 0
	listTemp.clear()
	if count > len(listUnique):
		print "count: " + str(count) + " length of listUnique: " + str(len(listWithLine))
		count = len(listUnique)
		timesOfReduce += 1


	analysis.write("Used: " + str(timesOfReduce) + " sentence(s) now\n")
	analysis.write("\n")
	#print listUnique

	if rate >= 0.75:
		if writeUniqueList == 0:
			for k, v in listUnique.iteritems():
				print '%s' % (k)
    			scripts.write('%s' % (k))
		#scripts.write(listUnique)
			writeUniqueList = 1

	sentenceNumArray.append(timesOfReduce)
	coverageArray.append(rate*100)

dest1.close()
analysis.close()
scripts.close()

#print sentenceNumArray
#print coverageArray

#======================================================================
# sns.set(color_codes=True)
# sns.lmplot(x = "Number of Sentences", y = "Words Covered Rate(%)", col)

sns.set(color_codes=True)
sns.set_style("darkgrid")
plt.plot(sentenceNumArray, coverageArray)
plt.axis([0,countResult,0,100])
plt.xlabel('Number of Sentences')
plt.ylabel('Words Covered Rate (%)')
plt.show()

# with open('abkTNew.txt') as infile:
# 	c = infile.read()
# 	for word in c.split('\n'):
# 		countResult += 1

print "total sentence number:"
print countResult
result = float(timesOfReduce) / float(countResult)
result *= 100

print str(timesOfReduce) + " times to cover all the unique words by going through "+ str(countResult)+" sentences"
print "precentage is: " + str(int(result)) + "%"

## put sentence into hashmap and increase the count in values
## find smallest appear and all same number sentence with together
## then remove words from unique list
## find the lessest frequency in the list and compare with others 
## check if there has anything left, if yes 
	## find again
	## else return cover all the unique words
## ideal will be 10%




