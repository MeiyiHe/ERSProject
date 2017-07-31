import sys
from get_phoneme import get_phoneme

#change unicode to ascii
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

                            }
    return text.decode('utf-8').translate(uni2ascii).encode('ascii')

#print unicodetoascii("weren\xe2\x80\x99t")  


tags = {'AA':1, 'W':2, 'DH':3, 'AY':4, 'HH':5, 'CH':6, 'JH':7, 'ZH':8, 'EH':9, 'NG':10, 
'TH':11, 'IY':12, 'B':13, 'AE':14, 'D':15, 'G':16, 'F':17, 'AH':18, 'K':19, 'M':20,
'L':21, 'AO':22, 'N':23, 'IH':24, 'S':25, 'R':26, 'EY':27, 'T':28, 'AW':29, 'V':30, 
'Y':31, 'Z':32, 'ER':33, 'P':34, 'UW':35, 'SH':36, 'UH':37, 'OY':38, 'OW':39}


def addTags( input_file, input_dict, output_file ):

	#split into lines
	with open(input_file) as f:

		contents = f.read()

		contents = unicodetoascii(contents)
		contents = contents.replace("\n"," ")
		contents = contents.replace("'","")

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

		#save to the output file
		output = open(output_file,'w')
		output.write(contents[:-1].lower())
		print(contents[:-1].lower())
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
		output.write(content[1:])
		print(content[1:])
		output.close()

#addTags("wewe.txt", "wewe_PHONEMES.txt", "wewe_withTag.txt")
#addTags("abk_1705010000.txt", "abk_1705010000_PHONEMES.txt", "abk_1705010000_withTag.txt")


