from textPreprocess import preprocess
from pydub import AudioSegment
import os.path
import sys

if len(sys.argv) != 2:
	print("Not enough arguments!")
	print("Format: python filename.txt output.wav")
	sys.exit(-1)

#Process the script file
preprocess(sys.argv[1])
print("txt processed.")
print()

script = open("output.txt")
lines = []
print (lines)
index = 0
for line in script.readlines(): #For each line
	words = line.split()
	number_words = len(words)
	counts = [0]*number_words
	print()
	print("The array used to store counts: {}".format(counts))
	print ("The number of words in the line is {}".format(number_words))
	for i in range(number_words):   #For each words in the line
		for j in range(number_words-i):
			
			string = ' '.join(words[j:i+j+1])
			print("Looking for the file - {}.wav".format(string.lower()))
			#check if the file exists
			if os.path.isfile("./out/{}.wav".format(string.lower())):
				counts[j] += 1
	print ("The new array: {}".format(counts))


	#select the best combination
	i=0
	print()
	lines.append([])
	total = 0
	while total < len(counts):
		print("i and count[i] is {}, {}".format(i, i+counts[i]))
		print(' '.join(words[i:i+counts[i]]).lower())
		lines[index].append(' '.join(words[i:i+counts[i]]).lower())
		print (lines)
		total += counts[i]
		i = i+counts[i]
		print(i)
		
	print("This will be: {}".format( lines[index] ))
	index += 1

#Concatenate
combined = AudioSegment.from_file("./out/"+lines[0][0]+".wav")
for i in range(len(lines)):
	for j in range(len(lines[i])):
		if i == 0 and j==0:
			continue
		combined += AudioSegment.from_file("./out/"+lines[i][j]+".wav")

combined.export("Output.wav", format="wav")



