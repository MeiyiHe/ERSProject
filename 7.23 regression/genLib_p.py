#for sentences
#read timestamps and split the audios into chunks

from pydub import AudioSegment
from itertools import islice
from textPreprocess import preprocess
from add_tag import unicodetoascii
from get_timestamps import get_timestamps_p
import subprocess
import wave
import sys
import time
import os

def genLib_p(username, input_file):

	#clock
	start_time = time.time()

	p="Prosodylab-Aligner"
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	lab = p+"/data/"+input_file+".lab"                                       #Prosodylab-Aligner/data/abk_1705010000.lab
	TG = p+"/data/"+input_file+".TextGrid"                                   #Prosodylab-Aligner/data/abk_1705010000.TextGrid
	preprocessed_script = username+"/"+input_file+"_preprocess.txt"          #abk/abk_1705010000_preprocess.txt
	timestamps_file = username+"/"+input_file+"_TIMESTAMPS.txt"              #abk/abk_1705010000_TIMESTAMPS.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_p"                                          #abk/GL_p

	#clean the data folder
	subprocess.call('rm -rf {}/data/*'.format(p), shell=True)

	#convert txt script to lab script (used in aligner)
	script_r = open(script)
	contents = unicodetoascii(script_r.read())
	contents = contents.replace("'",' ')
	contents = ''.join(ch for ch in contents if ch not in ('!','.',':',',',';'))
	contents = ' '.join(contents.split('\n'))
	contents = ' '.join(contents.split())
	contents = contents.upper()
	script_r.close()

	lab_w = open(lab,'w')
	lab_w.write(contents)
	lab_w.close()

	#copy the audio
	print(subprocess.check_output(['cp', soundinpath, p+"/data"]))

	###################################
	#         run the aligner         #
	###################################

	print("Running Prosody Aligner ... ... ")
	print('')
	#python3 -m aligner -r eng.zip -a data -d eng.dict
	os.chdir(p)
	#print(os.getcwd())
	print(subprocess.check_output(['python3','-m','aligner','-r','eng.zip','-a','data','-d','eng.dict']))
	os.chdir('..')
	#print(os.getcwd())

	#Process the script file
	preprocess(script)
	print('\n')
	print("txt processed.")

	#get the timestamps
	timestamps = get_timestamps_p(TG)

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
				segment.export(soundoutpath+"/"+string.lower()+".wav", format="wav")

		total += count

	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

#genLib_p('abk', 'abk_1705010000')
#genLib_p('abk', '170720_001')





