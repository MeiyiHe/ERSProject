import argparse
from functions import *
import os.path
import time
import sys

def covering_m_phon(username, filename, cost, pause, end, rate, output_folder):

	print("Covering by Montreal + phoneme tags ... ... ")

	#clock
	start_time = time.time()

	inputDir = username+"/GL_m_phon"                         				   #abk/GL_m_phon
	dicts = "montreal-forced-aligner/dicts"
	if end == '0':
		output_file = username+'_['+filename[:-4]+']_m_phon'+cost+'_'+pause[0]+'_'+str(rate)
		tag_script = filename[:-4]+"_m_phonTag.txt"
	else:
		output_file = username+'_['+filename[:-4]+']_m_phon'+cost+'_'+pause[0]+'_'+str(rate)+'_withEnd'+end
		tag_script = filename[:-4]+"_m_withEnd"+end+"_phonTag.txt"

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	phonTags(filename, dicts, tag_script,'m', end)  #always input dicts as a directory(current)
	print("txt processed.")
	print('')

	#covering
	lines = cover_phon(tag_script, inputDir, cost, rate)

	#Concatenate
	combined = AudioSegment.silent(duration=0)
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			
			if "<pause" in lines[i][j] and ">" in lines[i][j]:			
				pause = lines[i][j][1:len(lines[i][j])-1]
				match = re.match(r"([a-z]+)([0-9]+)",pause,re.I)
				if pause == 'natural':				
					audio = AudioSegment.from_wav(inputDir+'/<pause>.wav')
				else:
					audio = AudioSegment.silent(duration=14000)
				if match:
					t = match.group(2) #number
					combined += audio[:float(t)]
				else:
					combined += audio[:1000]		
				continue			

			combined += AudioSegment.from_wav("./{}/".format(inputDir)+lines[i][j])

	if output_folder != None:
		if not os.path.isdir(output_folder):
			os.makedirs(output_folder)
		combined.export("{}/{}.wav".format(output_folder, output_file), format="wav")
	else:
		combined.export("{}.wav".format(output_file), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

def covering_m_punc(username, filename, pause, end, output_folder):

	print("Covering by Montreal + punctuation tags ... ... ")

	#clock
	start_time = time.time()

	script_r = filename
	inputDir = username+"/GL_m_punc"                          #abk/GL_m_punc
	if end == '0':
		output_file = username+'_['+filename[:-4]+']_m_punc_'+pause[0]
		tag_script = script_r[:-4]+"_m_puncTag.txt"
	else:
		output_file = username+'_['+filename[:-4]+']_m_punc_'+pause[0]+'_withEnd'+end
		tag_script = script_r[:-4]+"_m_withEnd"+end+"_puncTag.txt"

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	puncTags(script_r, tag_script, 'm', end)
	print("txt processed.")
	print('')

	#covering
	lines = cover_punc(tag_script, inputDir)

	#Concatenate
	combined = AudioSegment.silent(duration=0)
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			
			if "<pause" in lines[i][j] and ">" in lines[i][j]:			
				pause = lines[i][j][1:len(lines[i][j])-1]
				match = re.match(r"([a-z]+)([0-9]+)",pause,re.I)				
				if pause == 'natural':				
					audio = AudioSegment.from_wav(inputDir+'/<pause>.wav')
				else:
					audio = AudioSegment.silent(duration=14000)
				if match:
					t = match.group(2) #number
					combined += audio[:float(t)]
				else:
					combined += audio[:1000]		
				continue			

			combined += AudioSegment.from_wav("./{}/".format(inputDir)+lines[i][j]+".wav")

	if output_folder != None:
		if not os.path.isdir(output_folder):
			os.makedirs(output_folder)
		combined.export("{}/{}.wav".format(output_folder, output_file), format="wav")
	else:
		combined.export("{}.wav".format(output_file), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))


def covering_p_punc(username, filename, pause, end, output_folder):

	print("Covering by Prosody + punctuation tags ... ... ")

	#clock
	start_time = time.time()

	script_r = filename                                              #filename.txt
	inputDir = username+"/GL_p_punc"                                 #abk/GL
	if end == '0':
		output_file = username+'_['+filename[:-4]+']_p_punc_'+pause[0]
		tag_script = script_r[:-4]+"_p_puncTag.txt"
	else:
		output_file = username+'_['+filename[:-4]+']_p_punc_'+pause[0]+'_withEnd'+end
		tag_script = script_r[:-4]+"_p_withEnd"+end+"_puncTag.txt"

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	puncTags(script_r, tag_script, 'p', end)
	print("txt processed.")
	print('')

	lines = cover_punc(tag_script, inputDir)

	#Concatenate
	combined = AudioSegment.silent(duration=0)
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			
			if "<pause" in lines[i][j] and ">" in lines[i][j]:			
				pause = lines[i][j][1:len(lines[i][j])-1]
				match = re.match(r"([a-z]+)([0-9]+)",pause,re.I)				
				if pause == 'natural':				
					audio = AudioSegment.from_wav(inputDir+'/<pause>.wav')
				else:
					audio = AudioSegment.silent(duration=14000)
				if match:
					t = match.group(2) #number
					combined += audio[:float(t)]
				else:
					combined += audio[:1000]				
				continue			

			combined += AudioSegment.from_wav("./{}/".format(inputDir)+lines[i][j]+".wav")

	if output_folder != None:
		if not os.path.isdir(output_folder):
			os.makedirs(output_folder)		
		combined.export("{}/{}.wav".format(output_folder, output_file), format="wav")
	else:
		combined.export("{}.wav".format(output_file), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

def covering_p_phon(username, filename, cost, pause, end, rate, output_folder):

	print("Covering by Prosody + phoneme tags ... ... ")

	#clock
	start_time = time.time()

	tag_script = filename[:-4]+"_p_withEnd"+end+"_phonTag.txt"                #filename_p_phonTag.txt
	inputDir = username+"/GL_p_phon"                            #abk/GL_p_phon
	dicts = "montreal-forced-aligner/dicts"
	if end == '0':
		output_file = username+'_['+filename[:-4]+']_p_phon'+cost+'_'+pause[0]+'_'+str(rate)
		tag_script = filename[:-4]+"_p_phonTag.txt" 
	else:
		output_file = username+'_['+filename[:-4]+']_p_phon'+cost+'_'+pause[0]+'_'+str(rate)+'_withEnd'+end
		tag_script = filename[:-4]+"_p_withEnd"+end+"_phonTag.txt" 

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	phonTags(filename, dicts, tag_script,'p', end)  #always input dicts as a directory(current)
	print("txt processed.")
	print('')

	#covering
	lines = cover_phon(tag_script, inputDir, cost, rate)

	#Concatenate
	combined = AudioSegment.silent(duration=0)
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			
			if "<pause" in lines[i][j] and ">" in lines[i][j]:			
				pause = lines[i][j][1:len(lines[i][j])-1]
				match = re.match(r"([a-z]+)([0-9]+)",pause,re.I)				
				if pause == 'natural':				
					audio = AudioSegment.from_wav(inputDir+'/<pause>.wav')
				else:
					audio = AudioSegment.silent(duration=14000)
				if match:
					t = match.group(2) #number
					combined += audio[0:float(t)]
				else:
					combined += audio[0:1000]				
				continue			

			combined += AudioSegment.from_wav("./{}/".format(inputDir)+lines[i][j])

	if output_folder != None:
		if not os.path.isdir(output_folder):
			os.makedirs(output_folder)
		combined.export("{}/{}.wav".format(output_folder, output_file), format="wav")
	else:
		combined.export("{}.wav".format(output_file), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

#covering_m_phon('abk', 'covering_test_V1.txt', '1')
#covering_p_punc('abk', 'covering_test_V1.txt')
#covering_m_punc('abk', 'covering_test_V1.txt')
#covering_p_phon('abk', 'covering_test_V1.txt', '1')


parser = argparse.ArgumentParser(
	description="This program synthesizes a user-specific natural speech by inputting the username and a script to be synthesized.",
	epilog="Thanks for using our program.")
parser.add_argument('-u', nargs='?', type=str, default='abk', 
					help="username, default is 'abk'")                  
parser.add_argument('-f', nargs='?', type=str, required=True, 
					help="input_file - the file to be synthesized")
parser.add_argument('-a', choices=['m','p'], required=True,
					help="pick the user library generated by which aligner, [m-Montreal, p-Prosody]") 
parser.add_argument('-t', choices=['punc', 'phon'], required=True,
					help='pick the tagging to use [phon - phoneme tags, punc - punctuation tags]')
parser.add_argument('-cost', choices=['0','1','2'],
					help="three different cost matrices according to three different ways of grouping")
parser.add_argument('-pause', choices=['natural','silence'], default='natural',
					help="two different pauses to use [natural - silent recording, silence - complete silence]")
parser.add_argument('-end', default='0',
					help="add a short pause after the end of each sentence")
parser.add_argument('-rate', nargs='?', type=int, choices=range(0,101), default=50,
					help="different weights to the concatenation cost and the phoneme cost")
parser.add_argument('-o', nargs='?', type=str, help="output_folder - name the folder to store all the synthesized output")

#python covering.py -u abk -f covering_test_V1.txt -a m -cost 1 -t phon

args = parser.parse_args()
print(args)

username = args.u
input_file = args.f
aligner = args.a
cost = args.cost
tag = args.t
pause = args.pause
end = args.end
rate = args.rate
output_folder = args.o

#check if the user library exists
if not os.path.isdir(username):
	print("The user library - {} doesn't exist!".format(username))
	print("Please generate the user library first!")
	sys.exit(-1)

#check if the covering file exists
if not os.path.isfile(input_file):
	print("Sorry, cannot find the script to be synthesized!")
	sys.exit(-1)

if aligner == 'm' and tag == 'phon':
	if cost == None:
		print("Please choose one of the cost matrices!")
		sys.exit(-1)
	covering_m_phon(username, input_file, cost, pause, end, rate, output_folder)
elif aligner == 'm' and tag == 'punc':
	covering_m_punc(username, input_file, pause, end, output_folder)
	if cost != None:
		print('')
		print("Cost is specified, but it's not an attribute to puncTags!")
	if rate != 50:
		print(rate)
		print('')
		print("Rate is specified, but it's not an attribute to puncTags!")
elif aligner == 'p' and tag == 'punc':
	covering_p_punc(username, input_file, pause, end, output_folder)
	if cost != None:
		print('')
		print("Cost is specified, but it's not an attribute to puncTags!")
	if rate != 50:
		print('')
		print("Rate is specified, but it's not an attribute to puncTags!")
else: # aligner == 'p' and tag == 'phon'
	if cost == None:
		print("Please choose one of the cost matrices!")
		sys.exit(-1)
	covering_p_phon(username, input_file, cost, pause, end, rate, output_folder)


