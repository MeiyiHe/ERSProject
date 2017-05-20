import sys
import os
import string
import functools
import operator
import re
import time


dest = open('TNresult.txt','w')
num = 0
dotCount = 0
punctuationNum = 0
digitCount = 0
commaCount = 0
questionCount = 0
#punctuation_count = len(filter(functools.partial(operator.contains, punctuation), a))
with open('abkTalkNote.txt') as infile:
	c = infile.read()
	for char in c:
		if char.isdigit() == True:
			digitCount +=1
		elif char == '.':
			dotCount += 1
		elif char == ',':
			commaCount += 1
		elif char == '?':
			questionCount += 1
	
	line = c.split()
	num += len(line)
	uniqueWords = set(line)


print "Original File have: ", num
print "Dot in file: ", dotCount
print "Comma in file: ", commaCount
print "Digit in file: ", digitCount
print "Question Mark in file: ", questionCount
infile.close()

resultNum = 0
for word in uniqueWords:
	dest.write(word)
	resultNum += 1
	dest.write('\n')
print "Unique Words number: ", resultNum

dest.close()



noPunc = open('TNnoPunctuation.txt','w')
punctuations = set('''!()-[]{};:'"\,<>./?@#$%^&*_~''')
no_punct = ""
punc=set(",./;'?&-()\"")
with open('TNresult.txt') as infile:
	for line in infile:
		#if line in punc:
		strp=''.join(c for c in line if not c in punctuations)
		noPunc.write(strp.lower())
noPunc.close()



resultUniqueNum = 0
dest4 = open('TNnotDuplicate.txt','w')
s = set()
for line in open('TNnoPunctuation.txt'):
	if line not in s:
		dest4.write(line)
		resultUniqueNum += 1
		s.add(line)
dest4.close()

dest5 = open('TNsortedResult.txt', 'w')
infile = open('TNnotDuplicate.txt')
lst = infile.readlines()
lst.sort()

for item in lst:
	dest5.write(item)
dest5.close()







