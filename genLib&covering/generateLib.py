#for sentences
#read timestamps and split the audios into chunks

from pydub import AudioSegment
from itertools import islice
from textPreprocess import preprocess
import wave
import sys
import time

#read the timestamps file
def readTS( filename ):
	timestamps_file = open(filename)
	contents = timestamps_file.read()
	contents = contents[:-1]
	timestamps = [float(x) for x in contents.split(',')]
	return timestamps



'''
#PROESSING BEGINS
if len(sys.argv) != 3:
	print("Generate the library with the set of scripts, audios and timestamps."
	+ "\n\nUsage: %s username filename \n" % sys.argv[0])
	sys.exit(-1)
'''

def generateLib(username, filename):

	#clock
	start_time = time.time()

	username = sys.argv[1]                                                    #abk
	script = username+"/"+sys.argv[2]+".txt"                                  #abk/abk_1705010000.txt
	preprocessed_script = username+"/"+sys.argv[2]+"_preprocess.txt"          #abk/abk_1705010000_preprocess.txt
	timestamps_file = username+"/"+sys.argv[2]+"_TIMESTAMPS.txt"              #abk/abk_1705010000_TIMESTAMPS.txt
	soundinpath = username+"/"+sys.argv[2]+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL"                                             #abk/GL

	#Process the script file
	preprocess(script)
	print('\n')
	print("txt processed.")

	#get the timestamps
	timestamps = readTS( timestamps_file )	

	#Cut the audio according to the timestamps and the script
	txt = open(preprocessed_script)
	audio = AudioSegment.from_wav(soundinpath)
	total = 0
	#process line by line
	for lines in txt.readlines():

		words = lines.split()
		print('')
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
				string = ''.join(words[j:i+j+1])
				print("exporting...     "+string.lower()+".wav")
				segment.export(soundoutpath+"/"+string.lower()+".wav")

		total += count

	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))









