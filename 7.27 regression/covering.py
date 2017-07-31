import argparse
from functions import *
import os.path
import sys

def covering_m_phon(username, filename, cost):

	print("Covering by Montreal + phoneme tags ... ... ")

	#clock
	start_time = time.time()

	tag_script = filename[:-4]+"_m_withTag.txt"                 #filename_withTag.txt
	#covering_script = filename[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL_m_phon"                          #abk/GL_m_phon
	dicts = "montreal-forced-aligner/dicts"

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	addTags(filename, dicts, tag_script,'m')  #always input dicts as a directory(current)
	print("txt processed.")
	print('')

	#covering
	lines = cover_phon(tag_script, inputDir, cost)

	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0])
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j])

	combined.export("{}_m_phon{}_output.wav".format(filename[:-4], cost), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

def covering_m_punc(username, filename):

	print("Covering by Montreal + punctuation tags ... ... ")

	#clock
	start_time = time.time()

	script_r = filename
	preprocessed_script = script_r[:-4]+"_m_preprocess.txt"     #filename_preprocess.txt
	#covering_script = filename[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL_m_punc"                          #abk/GL_m_punc

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	preprocess(script_r, preprocessed_script, 'm')
	print("txt processed.")
	print('')

	#covering
	lines = cover_punc(preprocessed_script, inputDir)

	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0]+".wav")
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j]+".wav")

	combined.export("{}_m_punc_output.wav".format(filename[:-4]), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))


def covering_p_punc(username, filename):

	print("Covering by Prosody + punctuation tags ... ... ")

	#clock
	start_time = time.time()

	script_r = filename                                       #filename.txt
	preprocessed_script = script_r[:-4]+"_p_preprocess.txt"     #filename_preprocess.txt
	#covering_script = script_r[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL_p_punc"                                 #abk/GL

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	preprocess(script_r, preprocessed_script, 'p')
	print("txt processed.")
	print('')

	lines = cover_punc(preprocessed_script, inputDir)

	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0]+".wav")
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j]+".wav")

	combined.export("{}_p_punc_output.wav".format(script_r[:-4]), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

def covering_p_phon(username, filename, cost):

	print("Covering by Prosody + phoneme tags ... ... ")

	#clock
	start_time = time.time()

	tag_script = filename[:-4]+"_p_withTag.txt"                 #filename_withTag.txt
	#covering_script = filename[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL_p_phon"                          #abk/GL_p_phon
	dicts = "montreal-forced-aligner/dicts"

	if not os.path.isdir(inputDir):
		print("Sorry, {} doesn't exist.".format(inputDir))
		print("Please generate the specific user library first!")
		sys.exit(-1)

	#Process the script file
	addTags(filename, dicts, tag_script,'p')  #always input dicts as a directory(current)
	print("txt processed.")
	print('')

	#covering
	lines = cover_phon(tag_script, inputDir, cost)

	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0])
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j])

	combined.export("{}_p_phon{}_output.wav".format(filename[:-4], cost), format="wav")

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
#parser.add_argument('-o', nargs='?', type=str, help="output_folder - name the folder to store all the synthesized output")
parser.add_argument('-a', choices=['m','p'], required=True,
					help="pick the user library generated by which aligner, [m-Montreal, p-Prosody]") 
parser.add_argument('-t', choices=['punc', 'phon'], required=True,
					help='pick the tagging to use [phon - phoneme tags, punc - punctuation tags]')
parser.add_argument('-cost', choices=['0','1','2'],
					help="three different cost matrices according to three different ways of grouping")
#parser.add_argument('-rate', nargs='?', type=float, choices=range(0,1),
					#help="different weights to the concatenation cost and the phoneme cost") #additional problems may be introduced

#python covering.py -u abk -f covering_test_V1.txt -a m -cost 1 -t phon

args = parser.parse_args()
print(args)

username = args.u
input_file = args.f
#output_file = args.o
aligner = args.a
cost = args.cost
tag = args.t
#rate = args.rate

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
	covering_m_phon(username, input_file, cost)
elif aligner == 'm' and tag == 'punc':
	covering_m_punc(username, input_file)
elif aligner == 'p' and tag == 'punc':
	covering_p_punc(username, input_file)
else: # aligner == 'p' and tag == 'phon'
	if cost == None:
		print("Please choose one of the cost matrices!")
		sys.exit(-1)
	covering_p_phon(username, input_file, cost)


