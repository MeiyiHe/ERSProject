import string,os,sys


if len(sys.argv) != 2:
	print("Strip punctuation in target file"
	+ "\n\nUsage: %s inputText\n" % sys.argv[0])
	sys.exit(-1)


textFile = sys.argv[1]

with open(textFile, 'r') as text:
	content = text.read()
newfp = '{0}_processed{1}'.format(*os.path.splitext(textFile))
with open(newfp, 'w') as f:
      f.write(content.upper().translate(None,string.punctuation))
f.close()
