import sys

#add Tags
'''
Basic:
0 = prelimiary
1 = nothing special
2 = at start of sentence
3 = period end
4 = before comma
5 = after comma
6 = question mark end
7 = exclamation mark end
Combination:
8 = start and end at the same word                        (1+2) (ex.Good.)
9 = start & before comma                                  (1+3) (ex.Well,)
10 = start and end with question mark at the same word     (1+5) (ex.What?)
11 = start and end with exclamation mark at the same word (1+6) (ex.Excellent!)
12 = after & before comma                                 (4+3) (ex. dogs,| cats, | fish)
13 = after comma & at the end of the sentence             (2+4) (ex. power, reliability)
'''
def addTags(  input_file, output_file ):

	#edit the input file
	contents = open(input_file).read()

	#remove extra spaces
	contents = ' '.join(contents.split())

	#initialize tags
	begin_tag = 1
	AC_tag = 0

	#adding tags
	contents = contents.replace('-',' ')
	words = contents.split()
	for i in range(len(words)):
	
		#skip special tags
		if words[i] == "<pause>":
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
	print("first edition with tags:")
	print(contents)

#whenever a symbol occurs, change the symbol to a new line character
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
	contents = '\n'.join(contents.split('-1 '))
	contents = '\n'.join(contents.split('/ '))
	contents = '\n'.join(contents.split('( '))
	contents = '\n'.join(contents.split(') '))
	contents = '\n'.join(contents.split('[ '))
	contents = '\n'.join(contents.split('] '))
	contents = '\n'.join(contents.split('{ '))
	contents = '\n'.join(contents.split('} '))

	#without spaces
	contents = '\n'.join(contents.split(','))
	contents = '\n'.join(contents.split('.'))
	contents = '\n'.join(contents.split('?'))
	contents = '\n'.join(contents.split('!'))
	contents = '\n'.join(contents.split(':'))
	contents = '\n'.join(contents.split(';'))
	contents = '\n'.join(contents.split('-1'))
	contents = '\n'.join(contents.split('/'))
	contents = '\n'.join(contents.split('('))
	contents = '\n'.join(contents.split(')'))
	contents = '\n'.join(contents.split('['))
	contents = '\n'.join(contents.split(']'))
	contents = '\n'.join(contents.split('{'))
	contents = '\n'.join(contents.split('}'))

	#special cases
	contents = contents.replace('"','')  #delete quotation marks
	contents = contents.replace("'",'')  #ex.cat's -> cats 
	contents = contents.replace(' and1', '\nand1')
	contents = contents.replace(' that1', '\nthat1')
	contents = '\n'.join(part for part in contents.split('\n') if part != '')

	#save to the output file
	output = open(output_file,'w')
	output.write(contents)
	output.close()

	print('\n')
	print("second edition to lines:")
	print(contents)

#Being imported to another file
def preprocess(filename):

	#create a new file to store the output
	output = filename[:-4] + "_preprocess.txt"

	#add tags
	addTags(filename, output)

	#put each sentence to a single line
	toLines(output, output)

def preprocessW(filename):

	#create a new file to store the output
	output = filename[:-4] + "_preprocess.txt"

	#edit the input file
	contents = open(filename).read()
	#print(type(contents))
	contents = '0\n'.join(contents.split())

	#save to the output file
	output = open(output,'w')
	output.write(contents+'0')
	output.close()

#preprocessW("abk/word_abk_1705010000.txt")
preprocess("test.txt")