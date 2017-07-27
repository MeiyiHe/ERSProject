from add_tag import addTags
from pydub import AudioSegment
import os.path
import sys
import time
import copy
import re

def covering_m(username, filename):

	#clock
	start_time = time.time()

	tag_script = filename[:-4]+"_withTag.txt"                 #filename_withTag.txt
	covering_script = filename[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL_m"                               #abk/GL_m
	dicts = username+"/dicts"                                 #abk/dicts

	'''
	same_cost - 0
	similar_beginning_cost - 1
	similar_phonate_area_cost - 2
	not_same_cost - 3
	concatenation_cost - 1 (extra)
	'''
	#cost matrix cost[need][actual]
	#use     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
	cost = [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 0
	        [0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 1
	        [0, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3],#need tag 2
	        [0, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 3
	        [0, 1, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 4
	        [0, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 5
	        [0, 3, 3, 3, 3, 3, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 6
	        [0, 3, 3, 3, 3, 3, 2, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 7
	        [0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3],#need tag 8
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 9
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 10
	        [0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 11
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 12
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 13
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 14
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 15
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 16
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 17
	        [0, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 18
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 19
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 20
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 21
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3],#need tag 22
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 23
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 24
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],#need tag 25
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 26
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 27
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 28
	        [0, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 29
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 30
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 31
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3],#need tag 32
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 1],#need tag 33
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3],#need tag 34
	        [0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 2, 3, 3],#need tag 35
	        [0, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3],#need tag 36
	        [0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 0, 3, 3],#need tag 37
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3],#need tag 38
	        [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 0]]#need tag 39
	        
	#NOTE: use 0_tag to substitue other tags will be assumed to be perfect

	#Process the script file
	addTags(filename, dicts, tag_script)  #always input dicts as a directory(current)
	print("txt processed.")
	print('')

	script = open(tag_script)
	lines = []
	print (lines)
	index = 0
	for line in script.readlines(): #For each line

		words = line.split()
		number_words = len(words)
		min_cost = []
		min_str = []

		for i in range(number_words):

			string_need = ''                      #the perfect string looked for
			need_tag = ''                         #the perfect tag for the string
			line_min_cost = []                    #the list used to store the least cost for each word count
			line_min_str = []                     #the corresponding string to the previous list

			pre_cost = i-1
			for j in range(i+1):
				print("i-{}, j-{}".format(i,j))

				#get the correct string
				match = re.match(r"([a-z]+)([0-9]+)",words[i-j],re.I)
				if match:
					if j==0:
						string_look = match.group(1).lower() + string_need
						string_need = words[i-j].lower() + string_need
						need_tag = match.group(2)
					else:
						string_look = match.group(1).lower() + "1" + string_look
						string_need = match.group(1).lower() + "1" + string_need
				print("string needed - {}".format(string_need))
				print("string look for - {}".format(string_look))

				#look for the files
				print("Looking for the file  - {}*.wav".format( string_look ))
				for file in os.listdir(inputDir):
					my_regex = re.escape(string_look) + r"([0-9]+).wav"
					match = re.match(my_regex,file)
					if match:
						use_tag = match.group(1)
						#costt = current cost + previous cost + concatenation cost
						if pre_cost < 0:
							costt = cost[int(need_tag)][int(use_tag)]
							string = [match.group(0)]
							
						else:
							costt = cost[int(need_tag)][int(use_tag)] + min_cost[pre_cost] +1
							#string = [min_str[pre_cost], [match.group(0)]]
							string = copy.deepcopy(min_str[pre_cost])
							string.append(match.group(0))
							
						line_min_cost.append(costt)
						line_min_str.append(string)
						print("Found {} with cost[{}][{}] {}".format(string, need_tag, use_tag, costt))
				pre_cost = pre_cost - 1
				print("line_min_cost - {}".format(line_min_cost))
				print("line_min_str - {}".format(line_min_str))
				print('')

			index = line_min_cost.index(min(line_min_cost))
			min_cost.append(line_min_cost[index])
			min_str.append(line_min_str[index])
			print("min_cost - {}".format(min_cost))
			print("min_str - {}".format(min_str))
			print('')
			print('')

		lines.append(min_str[len(min_str)-1])
		print(lines)

	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0])
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j])

	combined.export("{}_moutput.wav".format(filename[:-4]), format="wav")

	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))

#covering_m('abk','covering_test_V1.txt')



