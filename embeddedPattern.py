import os
from pydub import AudioSegment

#always start with pattern
#pattern - a directory with pattern voice files
#embed - an array of voice files to be embedded
def embeddedPattern(pattern, embed):

	#check if the directory exits
	if not os.path.exists(pattern):
		return 0

	#open an empty wav file to write
	output = wave.open("pattern_output.wav",'w')
	limit = len(embed)
	index = 0

	for file in os.listdir(pattern):

		output += AudioSegment.from_file(file)

		if index < len(embed) :
			embed_file = embed[index]+".wav"
			if os.path.isfile(embed_file)
			output += AudioSegment.from_file(embed_file)
		else:
			continue

		index++;

	return output

#TODO how to handle the case that start with embed

#test the function
#input: script with the pattern
#output: output voice files
#python embeddedPattern.py filename.txt outputDir
filename = sys.argv[1]
file = open(filename,'r')
words = file.split()
embed = []
for i in range(len(words)):
	if i==0:
		pattern = words[i]
		continue

	embed = embed.append(words[i]) 

# call the function
embeddedPattern(pattern, embed)