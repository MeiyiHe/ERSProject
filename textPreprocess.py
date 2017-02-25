import sys

#remove extra space in the file
def removeExtraSpace( filename ):
	file = open(filename)
	contents = file.read()
	contents = ' '.join(contents.split())
	file.close()
	print()
	print (contents)
	return contents

#whenever a symbol occurs, change the symbol to a new line character
def toLines( filename ):
	file = open(filename).read()
	contents = str(file).replace('. ','\n')
	contents = contents.replace('? ','\n')
	contents = contents.replace(', ','\n')
	contents = contents.replace('! ','\n')
	contents = contents.replace("'",'')  #ex.cat's -> cats
	contents = contents.replace('.', '') #delete the period in the end of the paragraph
	print()
	print("second edition:")
	print (contents)
	return contents

'''
#Use this file separately
if len(sys.argv) != 2:
	print("$python textPreprocess.py filename.txt")
	sys.exit(-1)

#remove extra space
contents = removeExtraSpace(sys.argv[1])
output = open("output.txt",'w')
output.write(contents)
output.close()

#put each sentence to a single line
contents = toLines("output.txt") 
output = open("output.txt",'w')
output.write(contents)
output.close()
'''

#Being imported to another file
def preprocess(filename):
	contents = removeExtraSpace(filename)
	output = open("output.txt",'w')
	output.write(contents)
	output.close()

	#put each sentence to a single line
	contents = toLines("output.txt") 
	output = open("output.txt",'w')
	output.write(contents)
	output.close()





