#the final parse of .TextGrid files in a directory 
# Usage:
#	python3 parseTextGridDIR.py TG_DIR


from pydub import AudioSegment
from os.path import basename
import wave
import os,sys

#extract the string inside double quote
def doit(text):      
  import re
  matches=re.findall(r'\"(.+?)\"',text)
  return ",".join(matches)

#check if the number is float
def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False

folder = sys.argv[1]
for filename in os.listdir(folder):
	infilename = os.path.join(folder,filename)
	bs = os.path.splitext(infilename)[0]

	if not os.path.isfile(infilename): continue

	#convert text files
	if infilename.endswith('.TextGrid'):
		text=open(infilename, 'r')
		for line in text:
			if "item [2]" in line:
				break;

		lines_after = text.readlines()[6:]
		timestamps = []

		words = []
		
		for string in lines_after:
			for f in string.split():
				if isfloat(f):
					timestamps.append(f)
				if ord(f[0]) == 34:
					words.append(doit(f))

		print("text file processed.")
		#print(words)
		#print(timestamps)
		print(infilename)
		b = open(bs+"_TIMESTAMPS.txt",'w')
		for i in range(len(words)):
			if words[i] != "sil" and words[i] != "sp":
				#print(words[i])
				print(float(timestamps[2*i]), ",",float(timestamps[2*i+1]),",",end=" ")
				b.write(str(timestamps[2*i]))
				b.write(",")
				b.write(str(timestamps[2*i+1]))
				b.write(",")

		print("\n\n")





