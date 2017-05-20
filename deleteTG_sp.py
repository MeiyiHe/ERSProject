# Analyze the output(.TextGrid) from first-time prosody aligner and deleting 
# all short pauses longer than 0.13 second in the wav audio 
# Usage:
#	python3 parseTextGridDIR.py TG_DIR 
# 			TG_DIR is a directory containing .TextGrid files, .wav files and .txt files
from pydub import AudioSegment
from os.path import basename
import wave
import os,sys
from decimal import *



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


folder = sys.argv[1]

for filename in os.listdir(folder):
	infilename = os.path.join(folder,filename)
	bs = os.path.splitext(infilename)[0]

	if not os.path.isfile(infilename): continue

	if infilename.endswith('.TextGrid'):
		# read complete text from .txt
		
		no_lim = []
		buff = []

		# analyze .TextGrid 
		text = open(infilename, 'r')

		audio = AudioSegment.from_wav(bs + ".wav")

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
					words.append(doit(f))
		 

		print("text file processed.")
		count = 1

		#for i in range(len(words)):
			#if words[i] != "sil" and words[i] != "sp":

				#print(float(timestamps[2*i]), ",",float(timestamps[2*i+1]),",",end=" ")

		print("\n\n")
		count = 0
		splitting = [0.0]

		buf = 0
		total = []
		content_words = []

		# getting timestamps of separate paragraphs
		for i in range(len(words)):
			if words[i] != "sil" and words[i] != "sp":
				content_words.append(words[i])
				buf += 1
			if words[i] == "sil":
				splitting.append(Decimal(timestamps[2*i]))
				splitting.append(Decimal(timestamps[2*i+1]))	
				count += 1
			# version 2 begin
			if words[i] == "sp" and Decimal(timestamps[2*i+1]) - Decimal(timestamps[2*i]) > 0.13:
				splitting.append(Decimal(timestamps[2*i]))
				splitting.append(Decimal(timestamps[2*i+1])) # version 2 end	
				count += 1
		all_audio=AudioSegment.empty()
		if count > 0:
			print("CURRENT FILE IS")
			print(bs)
			print("\n")
			splitting.append(len(audio)/1000)
			for i in range(int(len(splitting)/2)):
				start_ms = float(splitting[2*i])*1000
				end_ms = float(splitting[2*i+1])*1000
				audio_tmp = audio[start_ms:end_ms]
				all_audio = all_audio + audio_tmp

			all_audio.export(bs+".wav")

"""version 1 
			if words[i] == "sp" and words[i+2] == "sp":
				sp1_length = Decimal(timestamps[2*i+1]) - Decimal(timestamps[2*i])
				sp2_length = Decimal(timestamps[2*(i+2)+1]) - Decimal(timestamps[2*(i+2)])
				word_length = Decimal(timestamps[2*(i+1)+1]) - Decimal(timestamps[2*(i+1)])

				if(min(sp1_length,sp2_length)/word_length > 1 and word_length < 0.4) :
					count += 1
					
					print("\nword is ", words[i+1])
					splitting.append(Decimal(timestamps[2*i]))
					splitting.append(Decimal(timestamps[2*(i+2)+1]))
					print("\n")"""



