#!/usr/bin/env python
# File Name: countWordNumInFile.py
# Author: Meiyi (Lexi) He
# Description: A program that count number of words in each file
# To Compile & Run : python countWordNumInFile.py 
# output: number of words in the file 

from collections import Counter


# let user to input thw file name that they want to count
fname1 = raw_input("file that you want to count the number of words: ") 
# open the file
f1 = open(fname1)

# initial a counter
c = Counter()

with open(fname1, 'rb') as f:
    for ln in f:
        c.update(ln.split())

total1 = sum(c.values())
print total1


#####################################################################
'''
fname2 = raw_input("SR Scripts to be compared : ")
f2 = open(fname2)
c = Counter()
with open(fname2, 'rb') as f:
    for ln in f:
        c.update(ln.split())

total2 = sum(c.values())
print total2

'''
