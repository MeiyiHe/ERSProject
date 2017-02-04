#!/usr/bin/env python
# File Name: numToWords.py
# Author: Meiyi (Lexi) He
# Description: A program that convert all number to words
# To Compile & Run : python numToWords.py 
import os
import sys,math

def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
             'seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
            'eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+' ')
    if join: return ' '.join(words)
    return words


# open the file first
filename = raw_input("File that you want to convert all num to words: ") 

if filename and os.path.isfile(filename):
  with open(filename, 'r') as f:
    newfile = '{0}_NoNumber{1}'.format(*os.path.splitext(filename))
    with open(newfile, 'w') as f1:
        for word in f.read().split():
            if word.isdigit():
                print("there is a word")
                f1.write(numToWords(int(word)))
                f1.write(' ')
            else:
                f1.write(word)
                f1.write(' ')
    f1.close()
    f.close()















