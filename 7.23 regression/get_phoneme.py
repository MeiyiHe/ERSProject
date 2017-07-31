import sys
import re
import os.path

def get_phoneme(input_file, input_dict):

	#read the script
	file = open(input_file)
	out = "".join(c for c in file.read() if c not in ('!','.',':',"'"))

	#input_dict is a directory
	if os.path.isdir(input_dict):
		#read dictionaries
		p_pre = []
		for f in os.listdir(input_dict):
			p_file = open(os.path.join(input_dict, f))
			for line in p_file.readlines():
				p_pre.append(line.split())

	#input_dict is a file
	else:
		#read the dictionary
		p_file = open(input_dict)
		p_pre = []
		for line in p_file.readlines():
			p_pre.append(line.split())

	#align the phonemes with words in the script
	phoneme = []
	words = out.lower().split()
	for i in range(len(words)):
		found = 0
		for j in p_pre:
			if words[i]==j[0]:
				match = re.match(r"([a-z]+)([0-9]+)",j[1],re.I)
				if match:
					phoneme.append(match.group(1))
				else:
					phoneme.append(j[1])
				found = 1
				break
			else:
				continue
		if found == 0:
			print("NOT FOUND - {}".format(words[i]))
			sys.exit(-1)
	return phoneme
