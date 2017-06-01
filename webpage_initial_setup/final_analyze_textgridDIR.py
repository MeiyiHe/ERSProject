#!/usr/local/bin/python3
#the final parse of .TextGrid files in a directory 
# Usage:
#	python parseTextGridDIR.py TG_DIR

from pydub import AudioSegment
from os.path import basename
import wave
import os,sys

#extract the string inside double quote
def doit(text):      
  import re
  matches=re.findall(r'\"(.+?)\"',text)
  return ",".join(matches)

#check if the number is float
def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False


def grep_timestamp(folder):
	for filename in os.listdir(folder):
		infilename = os.path.join(folder,filename)
		bs = os.path.splitext(infilename)[0]

		if not os.path.isfile(infilename): continue

		#convert text files
		all_lines = []
		if infilename.endswith('.TextGrid'):
			text=open(infilename, 'r')
			for line in text:
				all_lines.append(line)
			target_index = 0
			for i in range(len(all_lines)):
				if "item [2]" in all_lines[i]:
					target_index = i

			timestamps = []
			words = []
			for i in range(len(all_lines)):
				if i > target_index + 6:
					for f in all_lines[i].split():
						if isfloat(f):
							timestamps.append(f)
						if ord(f[0]) == 34:
							words.append(doit(f))

			print "text file processed."
			#print(words)
			print timestamps
			print infilename
			b = open(bs+"_TIMESTAMPS.txt",'w')
			for i in range(len(words)):
				if words[i] != "sil" and words[i] != "sp":
					#print(words[i])
					#print(float(timestamps[2*i]), ",",float(timestamps[2*i+1]),",",end=" ")
					b.write(str(timestamps[2*i]))
					b.write(",")
					b.write(str(timestamps[2*i+1]))
					b.write(",")

			print "\n\n"





