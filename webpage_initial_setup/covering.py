from textPreprocess import preprocess
from pydub import AudioSegment
import os.path
import sys
import time

'''
if len(sys.argv) != 3:
	print("Not enough arguments!")
	print("Format: python username filename.txt")
	sys.exit(-1)
'''

def covering(username, filename):
	
	#clock
	start_time = time.time()

	script_r = filename                                   #filename.txt
	preprocessed_script = script_r[:-4]+"_preprocess.txt"     #filename_preprocess.txt
	covering_script = script_r[:-4]+"_covered.txt"			  #filename_covered.txt
	inputDir = username+"/GL"                                 #abk/GL

	#Process the script file
	preprocess(script_r)
	print("txt processed.")
	print('')

	script = open(preprocessed_script)
	lines = []
	print (lines)
	index = 0
	for line in script.readlines(): #For each line
		words = line.split()
		number_words = len(words)
		counts = [0]*number_words
		print('')
		print("The array used to store counts: {}".format(counts))
		print ("The number of words in the line is {}".format(number_words))
		for i in range(number_words):   #For each words in the line
			for j in range(number_words-i):
				
				string = ''.join(words[j:i+j+1])
				print("Looking for the file - {}.wav".format(string.lower()))
				#check if the file exists
				if os.path.isfile("./{}/{}.wav".format(inputDir, string.lower())):
					print("Exist!")
					counts[j] += 1

		print ("The array v_1: {}".format(counts))

		for i in range(len(counts)):
			if counts[i] == 0:
				string = words[i][:-1].lower()
				print "check_path"
				print "./{}/{}.wav".format(inputDir, string)

				if os.path.isfile("./{}/{}.wav".format(inputDir, string+'0')):
					words[i]=string+'0'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'1')):
					words[i]=string+'1'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'2')):
					words[i]=string+'2'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'3')):
					words[i]=string+'3'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'4')):
					words[i]=string+'4'
					counts[i] = 1			
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'5')):
					words[i]=string+'5'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'6')):
					words[i]=string+'6'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'7')):
					words[i]=string+'7'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'8')):
					words[i]=string+'8'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'9')):
					words[i]=string+'9'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'10')):
					words[i]=string+'10'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'11')):
					words[i]=string+'11'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'12')):
					words[i]=string+'12'
					counts[i] = 1
				elif os.path.isfile("./{}/{}.wav".format(inputDir, string+'13')):
					words[i]=string+'13'
					counts[i] = 1
				else:
					print("Cannot find {}!".format(words[i]))

		print ("The array v_2: {}".format(counts))

		for i in counts:
			if i==0:
				print " is missing {}".format(words[i])
				return words[i]

		#select the best combination
		i=0
		print('')
		lines.append([])
		total = 0
		count = 0
		while total < len(counts):
			print("i and count[i] is {}, {}".format(i, i+counts[i]))
			print(''.join(words[i:i+counts[i]]).lower())
			lines[index].append(''.join(words[i:i+counts[i]]).lower())
			print (lines)
			total += counts[i]
			i = i+counts[i]
			print(i)
			count += 1
			
		print("This will be: {}".format( lines[index] ))
		index += 1

	#write the covering result to a file
	cover_output = open(covering_script,'w')
	for each in lines:
		for w in each:
			cover_output.write(w)
			cover_output.write('\n')
		
	cover_output.close()


	#Concatenate
	combined = AudioSegment.from_file("./{}/".format(inputDir)+lines[0][0]+".wav")
	for i in range(len(lines)):
		for j in range(len(lines[i])):
			if i == 0 and j==0:
				continue
			combined += AudioSegment.from_file("./{}/".format(inputDir)+lines[i][j]+".wav")

	combined.export("{}_output.wav".format(script_r[:-4]), format="wav")

	return 1
	print("finished!")
	print("--- %s seconds ---" % (time.time() - start_time))



