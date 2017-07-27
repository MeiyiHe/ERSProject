#the final parse of .TextGrid files in a directory 
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

def get_timestamps_m(input_file):

	text=open(input_file, 'r')
	for line in text:
		if "item [1]" in line:
			break;

	lines_after = list(text)[5:]

	tier1_lines = []
	for string in lines_after:
		tier1_lines.append(string)
		if "item [2]" in string:
			break;

	timestamps = []
	words = []
	print("length of tier1_lines")
	print(len(tier1_lines))

	for string in tier1_lines:
		for f in string.split():
			if isfloat(f):
				timestamps.append(f)
			if ord(f[0]) == 34:
				words.append(doit(f))

	print("text file processed.")

	timestamps_n = []

	for i in range(len(words)):
		if words[i] != "":
			timestamps_n.append(timestamps[2*i])
			timestamps_n.append(timestamps[2*i+1])

	print(timestamps_n)
	print(len(timestamps_n))
	print("\n\n")

	return timestamps_n

#get_timestamps_m('abk/aligned/align/170720_001.TextGrid')

def get_timestamps_p(input_file):

	text=open(input_file, 'r')
	for line in text:
		if "item [2]" in line:
			break;

	lines_after = list(text)[6:]
	
	timestamps = []
	words = []
	
	for string in lines_after:
		for f in string.split():
			if isfloat(f):
				timestamps.append(f)
			if ord(f[0]) == 34:
				words.append(doit(f))

	print("text file processed.")

	timestamps_n = []
	for i in range(len(words)):
		if words[i] != "sil" and words[i] != "sp":
			#print(words[i])
			#print(float(timestamps[2*i]), ",",float(timestamps[2*i+1]),",", end=" ")
			timestamps_n.append(timestamps[2*i])
			timestamps_n.append(timestamps[2*i+1])

	print(timestamps_n)
	print(len(timestamps_n))
	print("\n\n")

	return timestamps_n

#get_timestamps_p('Prosodylab-Aligner/data/170720_001.TextGrid')





