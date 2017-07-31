from functions import *
import argparse
import time
import sys
import os.path
import subprocess


def genLib_m_phon(username, input_file):

	print("Generating the user library ( Montreal + phoneme tags ) ... ... ")
	
	#clock
	start_time = time.time()

	m = 'montreal-forced-aligner'
	TG = m+"/result/data/"+input_file+".TextGrid"                            #montreal-force-aligner/data/abk_1705010000.TextGrid
	lab = m+"/data/"+input_file+".lab"                                       #montreal-force-aligner/data/abk_1705010000.lab
	dic = m+"/dicts/"+input_file+"_m_dict"                                     #montreal-force-aligner/dicts/abk_1705010000_dict
	tag_script = username+"/"+input_file+"_m_withTag.txt"                      #abk/abk_1705010000_withTag.txt
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_m_phon"                                     #abk/GL_m_phon

	#run the aligner
	runM(m, dic, lab, script, soundinpath)

	#Process the script file
	addTags(script, dic, tag_script, 'm')
	print('\n')
	print("txt processed.")
	
	#get the timestamps
	timestamps = get_timestamps_m(TG)
	print(timestamps)

	#Cut the audio according to the timestamps and the script
	cut_phon(tag_script, timestamps, soundinpath, soundoutpath)

	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

	
def genLib_m_punc(username, input_file):

	print("Generating the user library ( Montreal + punctuation tags ) ... ... ")

	#clock
	start_time = time.time()

	m = 'montreal-forced-aligner'
	TG = m+"/result/data/"+input_file+".TextGrid"                            #montreal-force-aligner/data/abk_1705010000.TextGrid
	lab = m+"/data/"+input_file+".lab"                                       #montreal-force-aligner/data/abk_1705010000.lab
	dic = m+"/dicts/"+input_file+"_m_dict"                                     #montreal-force-aligner/dicts/abk_1705010000_dict
	preprocessed_script = username+"/"+input_file+"_m_preprocess.txt"          #abk/abk_1705010000_preprocess.txt
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_m_punc"                                     #abk/GL_m_phon

	#run the aligner
	runM(m, dic, lab, script, soundinpath)

	#Process the script file
	preprocess(script, preprocessed_script, 'm')
	print('\n')
	print("txt processed.")
	
	#get the timestamps
	timestamps = get_timestamps_m(TG)
	print(timestamps)

	#Cut the audio according to the timestamps and the script
	cut_punc(preprocessed_script, timestamps, soundinpath, soundoutpath)

	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))


def genLib_p_punc(username, input_file):

	print("Generating the user library ( Prosody + punctuation tags ) ... ... ")

	#clock
	start_time = time.time()

	p="Prosodylab-Aligner"
	TG = p+"/data/"+input_file+".TextGrid"                                   #Prosodylab-Aligner/data/abk_1705010000.TextGrid
	lab = p+"/data/"+input_file+".lab"                                       #Prosodylab-Aligner/data/abk_1705010000.lab
	preprocessed_script = username+"/"+input_file+"_p_preprocess.txt"          #abk/abk_1705010000_preprocess.txt
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_p_punc"                                     #abk/GL_punc

	#run the aligner
	runP(p, lab, script, soundinpath)	

	#Process the script file
	preprocess(script, preprocessed_script, 'p')
	print('\n')
	print("txt processed.")

	#get the timestamps
	timestamps = get_timestamps_p(TG)
	print(timestamps)
	print(len(timestamps))

	#Cut the audio according to the timestamps and the script
	cut_punc(preprocessed_script, timestamps, soundinpath, soundoutpath)
	
	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

def genLib_p_phon(username, input_file):

	print("Generating the user library ( Prosody + phoneme tags ) ... ... ")

	#clock
	start_time = time.time()

	p="Prosodylab-Aligner"
	m = 'montreal-forced-aligner'
	TG = p+"/data/"+input_file+".TextGrid"                                   #Prosodylab-Aligner/data/abk_1705010000.TextGrid
	lab_p = p+"/data/"+input_file+".lab"                                     #Prosodylab-Aligner/data/abk_1705010000.lab
	lab_m = m+"/data/"+input_file+".lab"                                     #montreal-force-aligner/data/abk_1705010000.lab
	dic = m+"/dicts/"+input_file+"_p_dict"                                     #montreal-force-aligner/dicts/abk_1705010000_dict
	tag_script = username+"/"+input_file+"_p_withTag.txt"                      #abk/abk_1705010000_withTag.txt
	script = username+"/"+input_file+".txt"                                  #abk/abk_1705010000.txt
	soundinpath = username+"/"+input_file+".wav"                             #abk/abk_1705010000.wav
	soundoutpath = username+"/GL_p_phon"                                     #abk/GL_punc

	#run the aligner
	runP(p, lab_p, script, soundinpath)
	#get the dic from Montreal
	genDic(m, dic, lab_m, script, soundinpath, 'p')

	#Process the script file
	addTags(script, dic, tag_script, 'p')
	print('\n')
	print("txt processed.")

	#get the timestamps
	timestamps = get_timestamps_p(TG)
	print(timestamps)
	print(len(timestamps))

	#Cut the audio according to the timestamps and the script
	cut_phon(tag_script, timestamps, soundinpath, soundoutpath)
	
	print(len(timestamps)/2)
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

#genLib_m_phon('abk','170720_001')
#genLib_p_punc('abk', '170720_001')
#genLib_m_punc('abk', '170720_001')
#genLib_p_phon('abk', '170720_001')


#############################################################################################################################
################################################    functions ended    ######################################################
#############################################################################################################################




#get arguments from the command line
parser = argparse.ArgumentParser(
	description="This program updates a user library by inputting a script and its corresponding audio.",
	epilog="Thanks for using our program.")
parser.add_argument('-u', nargs='?', default='abk', type=str,										
					help="username, default is 'abk'")                  
parser.add_argument('-f', nargs='?', type=str, required=True, 
					help="input_file(relative path) - the file used to generate the user library")
parser.add_argument('-a', choices=['m','p'], required=True, 
					help="pick the aligner to use [m-Montreal, p-Prosody]")
parser.add_argument('-t', choices=['phon','punc'], required=True, 
					help="pick the tagging to use [phon - phoneme tags, punc - punctuation tags]")

#python genLib.py -u abk -f 170720_001 -a m -t phon

args = parser.parse_args()

username = args.u
input_file = args.f
aligner = args.a
tag = args.t

#check if the user library exists
if not os.path.isdir(username):
	print("The user library - {} doesn't exist!\n".format(username))
	var = raw_input("If you want to create a new user library, please enter '1'.\n" \
					"If you want to exit, please enter'2'.\n\n"\
					"Please enter here:")
	print('')
	while(True):
		if var == '1':
			var = raw_input("Please enter the username:")
			print('')
			while (True):
				if var:
					yorn = raw_input("Is '{}' the username you want to input?[y/n]".format(var))
					print('')
					if yorn == 'y' or yorn == 'Y':
						#create the folder
						os.makedirs(var)
						print("Congratulations! The user library - {} is created!".format(var))
						print("Please put the files into the user library.")
						#break
						sys.exit(-1)
					elif yorn == 'n' or yorn == 'N':
						var = raw_input("Please reenter the username:")
						print('')
					else:
						print("Sorry, your input is not valid.\n")
				else:
					var = raw_input("Please enter the username:\n")
					print('')
			break
		elif var == '2':
			print("Thanks for using our program!")
			print("System is exiting ... ... ")
			sys.exit(-1)
		else:
			var = raw_input("Sorry, your input is invalid. Please input '1' or '2' only.\n" \
					"If you want to create a new user library, please enter '1'.\n" \
					"If you want to exit, please enter'2'.\n")


if aligner == 'm' and tag == 'phon':
	genLib_m_phon(username, input_file)
elif aligner == 'm' and tag == 'punc':
	genLib_m_punc(username, input_file)
elif aligner == 'p' and tag == 'punc':
	genLib_p_punc(username, input_file)
else: # aligner == 'p' and tag == 'phon'
	genLib_p_phon(username, input_file)



