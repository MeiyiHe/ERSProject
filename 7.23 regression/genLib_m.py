#for sentences
#read timestamps and split the audios into chunks

from pydub import AudioSegment
from add_tag import unicodetoascii
from itertools import islice
from add_tag import addTags
from get_timestamps import get_timestamps_m
import wave
import sys
import time
import re
import os.path
import string
import subprocess

def genLib_m(username, input_file):

	#clock
	start_time = time.time()

	m = 'montreal-forced-aligner'
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	lab = m+"/data/"+input_file+".lab"                                       #montreal-force-aligner/data/abk_1705010000.lab
	TG = m+"/result/data/"+input_file+".TextGrid"                                   #montreal-force-aligner/data/abk_1705010000.TextGrid
	dic = m+"/dicts/"+input_file+"_dict"                                     #montreal-force-aligner/dicts/abk_1705010000_dict
	tag_script = username+"/"+input_file+"_withTag.txt"                      #abk/abk_1705010000_withTag.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_m"                                          #abk/GL_m


	#clean the align folder
	subprocess.call('rm -rf {}/data/*'.format(m),shell=True)

	#convert txt script to lab script (used in aligner)
	script_r = open(script)
	contents = unicodetoascii(script_r.read())
	contents = ''.join(ch for ch in contents if ch not in ('!','.',':',',',"'",';','-'))
	contents = ' '.join(contents.split('\n'))
	contents = ' '.join(contents.split())
	contents = contents.upper()
	script_r.close()

	lab_w = open(lab,'w')
	lab_w.write(contents)
	lab_w.close()

	#copy the audio
	print(subprocess.check_output(['cp', soundinpath, m+"/data"]))

	###################################
	#         run the aligner         #
	###################################
	
	print("Running Montreal Forced Aligner ... ... ")
	print('')
	#bin/mfa_generate_dictionary model align-folder output_dict
	print("Generating the dictionary ... ... ")
	if not os.path.isdir('{}/data'.format(m)):
		os.makedirs('{}/data'.format(m))
	if not os.path.isdir('{}/dicts'.format(m)):
		os.makedirs('{}/dicts'.format(m))

	print(subprocess.check_output([m+'/aligner/bin/mfa_generate_dictionary', m+'/aligner/model_folder.zip', m+'/data', dic]))

	#bin/mfa_align align-folder output_dict english align_result-folder
	if not os.path.isdir('{}/result'.format(m)):
		os.makedirs('{}/result'.format(m))
	print("Align the script with the audio ... ... ")
	print(subprocess.check_output([m+'/aligner/bin/mfa_align', m+'/data',dic, 'english',m+'/result']))

	#Process the script file
	addTags(script, dic, tag_script)
	print('\n')
	print("txt processed.")
	
	#get the timestamps
	timestamps = get_timestamps_m(TG)

	#Cut the audio according to the timestamps and the script
	txt = open(tag_script)
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
				string = ''
				for k in range(j,i+j+1):
					if k==i+j:
						string += words[k]
						continue
					match = re.match(r"([a-z]+)([0-9]+)",words[k],re.I)
					if match:
						item = match.group(1) + '1'
						string += item
				print("exporting...     "+string.lower()+".wav")
				segment.export(soundoutpath+"/"+string.lower()+".wav", format="wav")

		total += count

	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))
	

#genLib_m('abk','abk_1705010000')







