#!/usr/bin/python
def getUniqueWord( file ):

	currFile = open(file)
	wordSet = set([word.strip(",.:;/?@#$%^&*_~'()-[]") for line in currFile for word in line.lower().split()])

	return wordSet


def checkCovered(curr, lib):

	set1 = getUniqueWord(curr)
	set2 = getUniqueWord(lib)

	# get the word from newFile, that have not covered by lib
	diff = set1 - set2

	if len(diff) == 0:
		print "Covered by Lib"
		return 1
		#return diff
	else:
		print "Not covered"
		return 0
		#return diff


def newWordSet(curr, lib):
	set1 = getUniqueWord(curr)
	set2 = getUniqueWord(lib)

	# get the symmetric difference 
	diff = set1 - set2

	return diff


def symmetricDifference(file1, file2):
	set1 = getUniqueWord(file1)
	set2 = getUniqueWord(file2)

	# get the symmetric difference 
	diff = set1 ^ set2

	if len(diff) == 0:
		print "NO difference"
		return diff
	else:
		print "difference:"
		return diff



#unique = uniqueList('abkTalkNote.txt')
#setCover('0530-note/5sen.txt')
#print newWordSet('0530-note/addNewLib.txt', '0530-note/11sen.txt')

#print symmetricDifference('0530-note/addNewLib.txt', 'meiyiFolder/Library.txt')






