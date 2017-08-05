from pydub import AudioSegment
from itertools import islice
import wave
import sys
import time
import copy
import re
import os.path
import string
import subprocess


#run the montreal aligner to get the dictionary (called within runM & genLib_p_phon)
def genDic(m, dic, lab, script, soundinpath, aligner):

	######################################### preparation for running the aligner ##############################################

	#clean the data folder
	if not os.path.isdir('{}/data'.format(m)):
		os.makedirs('{}/data'.format(m))
	subprocess.call('rm -rf {}/data/*'.format(m), shell=True)

	#convert txt script to lab script (used in aligner)
	script_r = open(script)
	contents = unicodetoascii(script_r.read())
	if aligner == 'm':
		contents = ''.join(ch for ch in contents if ch not in set(string.punctuation))
	else:
		contents = contents.replace("'",' ')
		contents = ''.join(ch for ch in contents if ch not in set(string.punctuation))
	contents = ' '.join(contents.split('\n'))
	contents = ' '.join(contents.split())
	contents = contents.upper()
	script_r.close()

	lab_w = open(lab,'w')
	lab_w.write(contents)
	lab_w.close()

	#copy the audio
	print(subprocess.check_output(['cp', soundinpath, m+"/data"]))

	################################################# Running Montreal #########################################################

	print("Running Montreal Forced Aligner ... ... ")
	print('')

	print("Generating the dictionary ... ... ")
	#bin/mfa_generate_dictionary model align-folder output_dict
	if not os.path.isdir('{}/dicts'.format(m)):
		os.makedirs('{}/dicts'.format(m))
	print(subprocess.check_output([m+'/aligner/bin/mfa_generate_dictionary', m+'/aligner/model_folder.zip', m+'/data', dic]))




#run the montreal aligner to get the TextGrid (called within genLib_m_phon & genLib_m_punc)
def runM(m, dic, lab, script, soundinpath):

	#generate the dictionary
	genDic(m, dic, lab, script, soundinpath, 'm')

	print("Align the script with the audio ... ... ")
	#bin/mfa_align align-folder output_dict english align_result-folder
	if not os.path.isdir('{}/result'.format(m)):
		os.makedirs('{}/result'.format(m))
	print(subprocess.check_output([m+'/aligner/bin/mfa_align', m+'/data',dic, 'english',m+'/result']))




#run the prosody aligner to get the TextGrid (called within genLib_p_phon & genLib_p_punc)
def runP(p, lab, script, soundinpath):

	######################################### preparation for running the aligner ##############################################

	#clean the data folder
	if not os.path.isdir('{}/data'.format(p)):
		os.makedirs('{}/data'.format(p))
	subprocess.call('rm -rf {}/data/*'.format(p), shell=True)

	#convert txt script to lab script (used in aligner)
	script_r = open(script)
	contents = unicodetoascii(script_r.read())
	contents = contents.replace("'",' ')
	contents = ''.join(ch for ch in contents if ch not in set(string.punctuation))
	contents = ' '.join(contents.split('\n'))
	contents = ' '.join(contents.split())
	contents = contents.upper()
	script_r.close()

	lab_w = open(lab,'w')
	lab_w.write(contents)
	lab_w.close()

	#copy the audio
	print(subprocess.check_output(['cp', soundinpath, p+"/data"]))

	################################################# Running Prosody #########################################################

	print("Running Prosody Aligner ... ... ")
	print('')
	#python3 -m aligner -r eng.zip -a data -d eng.dict
	os.chdir(p)
	#print(os.getcwd())
	print(subprocess.check_output(['python3','-m','aligner','-r','eng.zip','-a','data','-d','eng.dict']))
	os.chdir('..')
	#print(os.getcwd())




################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################




#change unicode to ascii (called within genDic(*.lab), runP(*.lab) & phonTags(*_phonTags.txt))
def unicodetoascii(text):

    uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),

            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),

            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),

            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),
            ord('\xef\xbc\x9a'.decode('utf-8')): ord(":"),

                            }
    return text.decode('utf-8').translate(uni2ascii).encode('ascii')

#print unicodetoascii("weren\xe2\x80\x99t")  




#get the phonemes from the dictionary (called within phonTags)
def get_phoneme(input_file, input_dict):

	#read the script
	file = open(input_file)
	out = "".join(c for c in file.read() if c not in ('!','.',':',"'"))

	#input_dict is a directory (covering)
	if os.path.isdir(input_dict):
		print("It's a directory")
		#read dictionaries
		p_pre = []
		for f in os.listdir(input_dict):
			p_file = open(os.path.join(input_dict, f))
			for line in p_file.readlines():
				p_pre.append(line.split())

	#input_dict is a file (genLib)
	else:
		print("It's a file")
		#read the dictionary
		p_file = open(input_dict)
		p_pre = []
		for line in p_file.readlines():
			p_pre.append(line.split())

	#align the phonemes with words in the script
	phoneme = []
	words = out.lower().split()
	for i in range(len(words)):

		if "<pause" in words[i] and ">" in words[i]:
			continue

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





tags = {'AA':1, 'W':2, 'DH':3, 'AY':4, 'HH':5, 'CH':6, 'JH':7, 'ZH':8, 'EH':9, 'NG':10, 
'TH':11, 'IY':12, 'B':13, 'AE':14, 'D':15, 'G':16, 'F':17, 'AH':18, 'K':19, 'M':20,
'L':21, 'AO':22, 'N':23, 'IH':24, 'S':25, 'R':26, 'EY':27, 'T':28, 'AW':29, 'V':30, 
'Y':31, 'Z':32, 'ER':33, 'P':34, 'UW':35, 'SH':36, 'UH':37, 'OY':38, 'OW':39}

#add tags (called within in genLib_m_phon & genLib_p_phon)
def phonTags( input_file, input_dict, output_file, aligner, end):

	#split into lines
	with open(input_file) as f:

		contents = f.read()

		contents = unicodetoascii(contents)
		print("Without editing:")
		print(contents)
		print('')
		contents = ' '.join(contents.split())        #to a single line
		contents = contents.replace('"', " ")        #remove double quotes
		contents = contents.replace('-', " ")
		contents = contents.replace('_', " ")

		if end != '0':
			contents = contents.replace('.', ".<pause"+end+">")

		if aligner == 'm':
			contents = contents.replace("'","")
		else:
			contents = contents.replace("'",' ')

		#with one space
		contents = '\n'.join(contents.split(', '))
		contents = '\n'.join(contents.split('. '))
		contents = '\n'.join(contents.split('? '))
		contents = '\n'.join(contents.split('! '))
		contents = '\n'.join(contents.split(': '))
		contents = '\n'.join(contents.split('; '))
		contents = '\n'.join(contents.split('/ '))
		contents = '\n'.join(contents.split('( '))
		contents = '\n'.join(contents.split(') '))
		contents = '\n'.join(contents.split('[ '))
		contents = '\n'.join(contents.split('] '))
		contents = '\n'.join(contents.split('{ '))
		contents = '\n'.join(contents.split('} '))
		contents = '\n<'.join(contents.split(' <'))
		contents = '>\n'.join(contents.split('> '))

		#without spaces
		contents = '\n'.join(contents.split(','))
		contents = '\n'.join(contents.split('.'))
		contents = '\n'.join(contents.split('?'))
		contents = '\n'.join(contents.split('!'))
		contents = '\n'.join(contents.split(':'))
		contents = '\n'.join(contents.split(';'))
		contents = '\n'.join(contents.split('/'))
		contents = '\n'.join(contents.split('('))
		contents = '\n'.join(contents.split(')'))
		contents = '\n'.join(contents.split('['))
		contents = '\n'.join(contents.split(']'))
		contents = '\n'.join(contents.split('{'))
		contents = '\n'.join(contents.split('}'))
		contents = '\n<'.join(contents.split('<'))
		contents = '>\n'.join(contents.split('>'))

		#remove extra spaces
		contents = '\n'.join(part for part in contents.split('\n') if part != '')
		contents = ' '.join(part for part in contents.split(' ') if part != '')

		#save to the output file
		output = open(output_file,'w')
		output.write(contents.lower())
		print("After editing - step 1:")
		print(contents.lower())
		print("")
		output.close()

	#get the phones
	phones = get_phoneme(output_file, input_dict)

	#add the tags
	content = ''
	with open(output_file) as f:
		contents = f.readlines()
		t=0
		for line in contents:

			if "<pause" in line and ">" in line:
				content = content + '\n' + line
				continue

			line_list = line.split()

			for i in range(len(line_list)):
				if i == len(line_list) - 1:
					line_list[i] = line_list[i]+'0'
					continue
				line_list[i] = line_list[i]+str(tags[phones[t+i+1].upper()])
				#print("{} follows the phoneme {}".format(line_list[i],phones[t+i+1].upper()))
				#print(t+1+i)
			t += len(line_list)
			content = content  + '\n'+' '.join(line_list)
		
		#save to the output file
		output = open(output_file,'w')

		content = content.replace(' and','\nand')
		content = content.replace(' that','\nthat')

		#remove extra spaces
		content = '\n'.join(part for part in content.split('\n') if part != '')
		content = ' '.join(part for part in content.split(' ') if part != '')

		output.write(content)
		print("After editing - step 2(final):")
		print(content)
		output.close()

#phonTags("abk/170720_001.txt", "montreal-forced-aligner/dicts/170720_001_m_dict", "abk/170720_001_m_withTag.txt",'m')




################################################################################################################################
################################################################################################################################
################################################################################################################################



#add punctuation tags (called within puncTags)
def addTag(  input_file, output_file , aligner, end):

	contents = open(input_file).read()

	contents = unicodetoascii(contents) 
	print("Without editing:")
	print(contents)
	print('')  
	contents = ' '.join(contents.split())    #to a single line
	contents = contents.replace('"', " ")	 #remove double quotes
	contents = contents.replace('-', " ")
	contents = contents.replace("_", " ")
	contents = contents.replace(">", "> ")
	contents = contents.replace("<", " <")

	if end != '0':
		contents = contents.replace('.', ". <pause"+end+">")

	if aligner == 'p':
		contents = contents.replace("'",' ')
	else:
		contents = contents.replace("'",'')

	#initialize tags
	begin_tag = 1
	AC_tag = 0

	words = contents.split()
	print("first split:{}".format(words))
	for i in range(len(words)):
	
		#skip special tags
		if "<pause" in words[i] and ">" in words[i]:
			continue

		#at the start of a sentence
		if begin_tag == 1:
			if '.' in words[i]:
				words[i] = words[i][:len(words[i])-1] + "8" + words[i][len(words[i])-1:]
			elif ',' in words[i]:
				words[i] = words[i][:len(words[i])-1] + "9" + words[i][len(words[i])-1:]
				begin_tag = 0
				AC_tag = 1
			elif '?' in words[i]:
				words[i] = words[i][:len(words[i])-1] + "10" + words[i][len(words[i])-1:]
			elif '!' in words[i]:
				words[i] = words[i][:len(words[i])-1] + "11" + words[i][len(words[i])-1:]
			else:
				words[i] = words[i] + "2"
				begin_tag = 0
		#period end
		elif '.' in words[i]:
			if AC_tag == 1:
				words[i] = words[i][:len(words[i])-1] + "13" + words[i][len(words[i])-1:]
				AC_tag = 0
			else:
				words[i] = words[i][:len(words[i])-1] + "3" + words[i][len(words[i])-1:]
			begin_tag = 1
		#before comma
		elif ',' in words[i]:
			if AC_tag == 1:
				words[i] = words[i][:len(words[i])-1] + "12" + words[i][len(words[i])-1:]
			else:
				words[i] = words[i][:len(words[i])-1] + "4" + words[i][len(words[i])-1:]
				AC_tag = 1
		#after comma
		elif AC_tag == 1:
			words[i] = words[i] + "5" 
			AC_tag = 0
		elif '?' in words[i]:
			words[i] = words[i][:len(words[i])-1] + "6" + words[i][len(words[i])-1:]
			begin_tag = 1
		elif '!' in words[i]:
			words[i] = words[i][:len(words[i])-1] + "7" + words[i][len(words[i])-1:]
			begin_tag = 1
		else:
			words[i] = words[i] + "1" 

		if ')' in words[i]:
			words[i] = ''.join(words[i].split(')')) + ')'
		if ']' in words[i]:
			words[i] = ''.join(words[i].split(']')) + ']'
		if '}' in words[i]:
			words[i] = ''.join(words[i].split('}')) + '}'
		if '>' in words[i]:
			words[i] = ''.join(words[i].split('>')) + '>'
		if ':' in words[i]:
			words[i] = ''.join(words[i].split(':')) + ':'
		if ';' in words[i]:
			words[i] = ''.join(words[i].split(';')) + ';'

	contents = ' '.join(words)

	#save to the output file
	output = open(output_file,'w')
	output.write(contents)
	output.close()

	print('\n')
	print("After editing - step 1:")
	print(contents)

#whenever a symbol occurs, change the symbol to a new line character (called within puncTags)
def toLines( input_file, output_file ):

	#edit the input file
	contents = open(input_file).read()

	#with one space
	contents = '\n'.join(contents.split(', '))
	contents = '\n'.join(contents.split('. '))
	contents = '\n'.join(contents.split('? '))
	contents = '\n'.join(contents.split('! '))
	contents = '\n'.join(contents.split(': '))
	contents = '\n'.join(contents.split('; '))
	contents = '\n'.join(contents.split('/ '))
	contents = '\n'.join(contents.split('( '))
	contents = '\n'.join(contents.split(') '))
	contents = '\n'.join(contents.split('[ '))
	contents = '\n'.join(contents.split('] '))
	contents = '\n'.join(contents.split('{ '))
	contents = '\n'.join(contents.split('} '))
	contents = '\n<'.join(contents.split(' <'))
	contents = '>\n'.join(contents.split('> '))

	#without spaces
	contents = '\n'.join(contents.split(','))
	contents = '\n'.join(contents.split('.'))
	contents = '\n'.join(contents.split('?'))
	contents = '\n'.join(contents.split('!'))
	contents = '\n'.join(contents.split(':'))
	contents = '\n'.join(contents.split(';'))
	contents = '\n'.join(contents.split('/'))
	contents = '\n'.join(contents.split('('))
	contents = '\n'.join(contents.split(')'))
	contents = '\n'.join(contents.split('['))
	contents = '\n'.join(contents.split(']'))
	contents = '\n'.join(contents.split('{'))
	contents = '\n'.join(contents.split('}'))
	contents = '\n<'.join(contents.split('<'))
	contents = '>\n'.join(contents.split('>'))

	#special cases
	contents = contents.replace(' and', '\nand')
	contents = contents.replace(' that', '\nthat')

	#remove extra spaces
	contents = '\n'.join(part for part in contents.split('\n') if part != '')
	contents = ' '.join(part for part in contents.split(' ') if part != '')

	#save to the output file
	output = open(output_file,'w')
	output.write(contents.lower())
	output.close()

	print('\n')
	print("After editing - step2(final):")
	print(contents.lower())
	print('')

#add tags (called within in genLib_m_punc & genLib_p_punc)
def puncTags(filename, preprocessed_script, aligner, end):

	#add tags
	addTag(filename, preprocessed_script, aligner, end)

	#put each sentence to a single line
	toLines(preprocessed_script, preprocessed_script)

#puncTags("abk/170720_001.txt", "abk/170720_001_m_preprocessed.txt",'p')




################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################




#extract the string inside double quote (called within get_timestamps_m & get_timestamps_p)
def doit(text):      
  import re
  matches=re.findall(r'\"(.+?)\"',text)
  return ",".join(matches)

#check if the number is float (called within get_timestamps_m & get_timestamps_p)
def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False





#extract time stamps from TextGrid (called within genLib_m_punc & genLib_m_phon)
def get_timestamps_m(input_file):

	text=open(input_file, 'r')
	for line in text:
		if "item [1]" in line:
			break;

	lines_after = list(text)[5:]

	tier1_lines = []
	for string in lines_after:
		tier1_lines.append(string)
		if "item [2]" in string:
			break;

	timestamps = []
	words = []
	print("length of tier1_lines")
	print(len(tier1_lines))

	for string in tier1_lines:
		for f in string.split():
			if isfloat(f):
				timestamps.append(f)
			if ord(f[0]) == 34:
				words.append(doit(f))

	print("text file processed.")

	timestamps_n = []

	for i in range(len(words)):
		if words[i] != "":
			timestamps_n.append(timestamps[2*i])
			timestamps_n.append(timestamps[2*i+1])

	print(timestamps_n)
	print(len(timestamps_n))
	print("\n\n")

	return timestamps_n

#get_timestamps_m('abk/aligned/align/170720_001.TextGrid')



#extract time stamps from TextGrid (called within genLib_p_punc & genLib_p_phon)
def get_timestamps_p(input_file):

	text=open(input_file, 'r')
	for line in text:
		if "item [2]" in line:
			break;

	lines_after = list(text)[6:]
	
	timestamps = []
	words = []
	
	for string in lines_after:
		for f in string.split():
			if isfloat(f):
				timestamps.append(f)
			if ord(f[0]) == 34:
				words.append(doit(f))

	print("text file processed.")

	timestamps_n = []
	for i in range(len(words)):
		if words[i] != "sil" and words[i] != "sp":
			#print(words[i])
			#print(float(timestamps[2*i]), ",",float(timestamps[2*i+1]),",", end=" ")
			timestamps_n.append(timestamps[2*i])
			timestamps_n.append(timestamps[2*i+1])

	print(timestamps_n)
	print(len(timestamps_n))
	print("\n\n")

	return timestamps_n




################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################




#cut the audio (called within genLib_m_phon & genLib_p_phon)
def cut_phon(tag_script, timestamps, soundinpath, soundoutpath):

	#open the tagged script
	txt = open(tag_script)
	audio = AudioSegment.from_wav(soundinpath)
	total = 0

	#check if soundoutpath exist
	if not os.path.isdir(soundoutpath):
		os.makedirs(soundoutpath)
		print(subprocess.check_output(['cp', '<pause>.wav',soundoutpath]))

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




#cut the audio (called within genLib_m_punc & genLib_p_punc)
def cut_punc(preprocessed_script, timestamps, soundinpath, soundoutpath):

	#open the preprocessed script
	txt = open(preprocessed_script)
	audio = AudioSegment.from_wav(soundinpath)
	total = 0

	#check if soundoutpath exist
	if not os.path.isdir(soundoutpath):
		os.makedirs(soundoutpath)
		print(subprocess.check_output(['cp', '<pause>.wav',soundoutpath]))

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




################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################




def cover_phon(tag_script, inputDir, cost, rate):

	###################################
	#           39 groups phoneme     #
	# same_cost - 0                   #
	# not_same_cost - 3               #
	# concatenation_cost - 1 (extra)  #
	###################################
	#cost matrix cost[need][actual]
	#use       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
	cost_0 = [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 0
	          [3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 1
	          [3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 2
	          [3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 3
	          [3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 4
	          [3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 5
	          [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 6
	          [3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 7
	          [3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 8
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 9
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 10
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 11
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 12
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 13
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 14
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 15
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 16
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 17
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 18
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 19
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 20
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 21
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 22
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 23
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 24
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 25
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 26
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 27
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 28
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 29
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 30
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 31
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3],#need tag 32
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],#need tag 33
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3],#need tag 34
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3],#need tag 35
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3],#need tag 36
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3],#need tag 37
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3],#need tag 38
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0]]#need tag 39

	###################################
	#           19 groups phoneme     #
	# same_cost - 0                   #
	# similar_beginning_cost - 1      #
	# similar_phonate_area_cost - 2   #
	# not_same_cost - 3               #
	# concatenation_cost - 1 (extra)  #
	###################################
	#cost matrix cost[need][actual]
	#use       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
	cost_1 = [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 0
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

	###################################
	#           6  groups phoneme     #
	# same_cost - 0                   #
	# same_group - 2                  #
	# not_same_cost - 3               #
	# concatenation_cost - 1 (extra)  #
	###################################
	#cost matrix cost[need][actual]
	#use       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
	cost_2 = [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 0
	          [3, 0, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 1
	          [3, 3, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 2
	          [3, 3, 3, 0, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 3
	          [3, 2, 3, 3, 0, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 4
	          [3, 3, 2, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 5
	          [3, 3, 3, 3, 3, 3, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 6 
	          [3, 3, 3, 3, 3, 3, 2, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 7
	          [3, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 8
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 9
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 10
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 11
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 0, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 12
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 2, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 13
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 0, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 14
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 0, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 15
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 16
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 17
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 0, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 18
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 19
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 20
	          [3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 21
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 0, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 22
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 23
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 0, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 24
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 25
	          [3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 26
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 0, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 27
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],#need tag 28
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 0, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2],#need tag 29
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 0, 3, 2, 3, 3, 3, 2, 3, 3, 3],#need tag 30
	          [3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3],#need tag 31
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 0, 3, 3, 3, 2, 3, 3, 3],#need tag 32
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 0, 3, 2, 3, 2, 2, 2],#need tag 33
	          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3],#need tag 34
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 0, 3, 2, 2, 2],#need tag 35
	          [3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 0, 3, 3, 3],#need tag 36
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 0, 2, 2],#need tag 37
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 0, 2],#need tag 38
	          [3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 2, 2, 0]]#need tag 39


	if cost == '0':
		cost = cost_0     #39 groups
	elif cost == '1':    
		cost = cost_1     #19 groups
	elif cost == '2':
		cost = cost_2     #6  groups
	else:
		print("The cost option is not valid! Your input is {}".format(cost))

	script = open(tag_script)
	lines = []
	print (lines)
	index = 0

	for line in script.readlines(): #For each line

		print(line)

		if "<pause" in line and ">" in line:
			lines.append(line.split())
			continue

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
							costt = (rate/100)*cost[int(need_tag)][int(use_tag)]
							string = [match.group(0)]
							
						else:
							costt = (rate/100)*cost[int(need_tag)][int(use_tag)] + min_cost[pre_cost] +(1-rate/100)*1
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

	return lines

def cover_punc(preprocessed_script, inputDir):

	script = open(preprocessed_script)
	lines = []
	print (lines)
	index = 0

	for line in script.readlines(): #For each line

		if "<pause" in line and ">" in line:
			lines.append(line.split())
			index += 1
			continue

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

		#select the best combination
		i=0
		print('')
		lines.append([])
		total = 0
		count = 0
		while total < len(counts):
			lines[index].append(''.join(words[i:i+counts[i]]).lower())
			total += counts[i]
			i = i+counts[i]
			count += 1
			
		print("This will be covered as: {}".format( lines[index] ))
		index += 1

	print('')
	print(lines)

	return lines
