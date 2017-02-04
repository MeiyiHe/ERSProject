#parse a text file with TextGrid format and export small chunks of wav files

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

#PROESSING BEGINS
if len(sys.argv) != 3:
	print("Parse a textgrid and Output related wav files."
	+ "\n\nUsage: %s inputDirectory outDirectory\n" % sys.argv[0])
	sys.exit(-1)


folder = sys.argv[1]
for filename in os.listdir(folder):
	infilename = os.path.join(folder,filename)
	if not os.path.isfile(infilename): continue

	#convert text files
	if infilename.endswith('.txt'):
		text=open(infilename, 'r')
		for line in text:
			if "item [2]" in line:
				break;

		lines_after = text.readlines()[6:]
		timestamps = []

		words = []
		for string in lines_after:
			for f in string.split():
				if isfloat(f):
					timestamps.append(f)
				if ord(f[0]) == 34:
					words.append(doit(f))

		print("text file processed.")

		soundinpath = os.path.join(folder,os.path.splitext(filename)[0] +".wav")
		soundoutpath = sys.argv[2]

		audio = AudioSegment.from_wav(soundinpath)

		for i in range(len(words)):
			start_ms=float(timestamps[2*i])*1000
			end_ms=float(timestamps[2*i+1])*1000

			segment = audio[start_ms:end_ms]
			if(words[i]!= "sil"):
				print("exporting..."+words[i]+".wav")
				segment.export(soundoutpath+"/"+words[i]+".wav")

		print("finished!")
"""
text = open(sys.argv[1], 'r')

#find signal keyword
for line in text:
    if "item [2]" in line:
    	break;
#skip useless lines
lines_after = text.readlines()[6:]

#processing useful lines
timestamps = []
words = []
for string in lines_after:
	for f in string.split():
		if isfloat(f):
			timestamps.append(f)
		#check if the char is double quote
		if ord(f[0])==34:
			words.append(doit(f));
 

print("text file processed.")

soundinpath = sys.argv[2]
soundoutpath = sys.argv[3]


audio = AudioSegment.from_wav(soundinpath)
for i in range(len(words)):
	start_ms=float(timestamps[2*i])*1000
	end_ms=float(timestamps[2*i+1])*1000

	segment = audio[start_ms:end_ms]
	if(words[i]!= "sil"):
		print("exporting..."+words[i]+".wav")
		segment.export(soundoutpath+"/"+words[i]+".wav")

print("finished!")
#PROCESSED
"""








