#for words
#read timestamps and split the audios into that of each words

from pydub import AudioSegment
from itertools import islice
from textPreprocess import preprocessW
import wave
import sys
import time

#read the timestamps file
def readTS( filename ):
	timestamps_file = open(filename)
	contents = timestamps_file.read()
	contents = contents[:-1]
	timestamps = [float(x) for x in contents.split(',')]  #delete the comma in the end of the file
	return timestamps

"""PROESSING BEGINS
if len(sys.argv) != 3:
	print("Generate the library with the set of scripts, audios and timestamps."
	+ "\n\nUsage: %s username filename \n" % sys.argv[0])
	sys.exit(-1)
"""
def generateLibW(username, filename):
	#clock
	start_time = time.time()
                                                 
	script = username+"/"+filename+".txt"                                  #abk/word_abk_1705010000.txt
	preprocessed_script = username+"/"+filename+"_preprocess.txt"          #abk/word_abk_1705010000_preprocess.txt
	timestamps_file = username+"/"+filename+"_TIMESTAMPS.txt"              #abk/word_abk_1705010000_TIMESTAMPS.txt
	soundinpath = username+"/"+filename+".wav"                             #abk/word_abk_1705010000.wav
	soundoutpath = username+"/GL"                                             #abk/GL

	#Process the script file
	preprocessW(script)
	print("txt processed.")

	#get the timestamps
	timestamps = readTS( timestamps_file )	

	#Cut the audio according to the timestamps and the script
	txt = open(preprocessed_script)
	audio = AudioSegment.from_wav(soundinpath)
	total = 0
	words = txt.read().split()

	#process line by line
	for i in range(len(words)):

		print("The word processed is {}".format(words[i]))

		start_ms=float(timestamps[2*i]*1000)
		print("The start time is {}".format(start_ms))
		end_ms=float(timestamps[2*i+1])*1000
		print("The ending time is {}".format(end_ms))

		segment = audio[start_ms:end_ms]
		print("exporting...     "+words[i].lower()+".wav")
		segment.export(soundoutpath+"/"+words[i].lower()+".wav")


	print(len(words))
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))
