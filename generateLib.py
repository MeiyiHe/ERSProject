#parse a text file with TextGrid format and export small chunks of wav files

from pydub import AudioSegment
from itertools import islice
from textPreprocess import preprocess
import wave
import sys

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
if len(sys.argv) != 5:
	print("Parse a textgrid and Output related wav files."
	+ "\n\nUsage: %s filename.TextGrid filename.txt originalAudio.wav outDirectory\n" % sys.argv[0])
	sys.exit(-1)
text = open(sys.argv[1], 'r')



#Read the next line and return the number of words

#Process the TextGrid

#find signal keyword
for line in text:
    if "item [2]" in line:
    	break;
#skip useless lines
next_6_lines = list(islice(text, 6))
print(next_6_lines)

timestamps = []
next_3_lines = list(islice(text, 3))
while next_3_lines:
	#chek if the valid entry
	words = next_3_lines[2].split()
	word = doit(words[2])

	if word[0].islower():
		text.readline()      #skip one line
		next_3_lines = list(islice(text, 3))
		continue

	#add times to timestamps
	words = next_3_lines[0].split()
	timestamps.append(words[2])
	words = next_3_lines[1].split()
	timestamps.append(words[2])
	text.readline()
	next_3_lines = list(islice(text, 3))

print("TextGrid processed.")



#Process the script file
preprocess(sys.argv[2])
print("txt processed.")



#Cut the audio according to the TextGrid and scripts

soundinpath = sys.argv[3]   #wav file
soundoutpath = sys.argv[4]  #output directory

txt = open("output.txt")
audio = AudioSegment.from_wav(soundinpath)
total = 0
#process line by line
c = 0
for lines in txt.readlines():
	words = lines.split()
	print()
	print("The line processed is {}".format(words))
	count = len(words)
	print("The number of words in the line is {}".format(count))
	for i in range(count): #number of words in each audio
		for j in range(count-i): #start at a certain word

			start_ms=float(timestamps[2*(j+total)])*1000
			print("The start time is {}".format(start_ms))
			end_ms=float(timestamps[2*(i+j+total)+1])*1000
			print("The ending time is {}".format(end_ms))

			segment = audio[start_ms:end_ms]
			string = ' '.join(words[j:i+j+1])
			print("exporting...     "+string.lower()+".wav")
			segment.export(soundoutpath+"/"+string.lower()+".wav")

	total += count
	if c==2:
		sys.exit(-1)
	c += 1



audio = AudioSegment.from_wav(soundinpath)
for i in range(len(words)):
	start_ms=float(timestamps[2*i])*1000
	end_ms=float(timestamps[2*i+1])*1000

	segment = audio[start_ms:end_ms]
	if(words[i]!= "sil"):
		#print("exporting..."+words[i].lower()+".wav")
		segment.export(soundoutpath+"/"+words[i].lower()+".wav")

print("finished!")
#PROCESSED









