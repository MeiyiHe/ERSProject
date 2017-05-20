import os,sys
from pydub import AudioSegment

if len(sys.argv) != 2:
	print("Convert all TextGrid files into .txt"
	+ "\n\nUsage: %s inputDirectory\n" % sys.argv[0])
	sys.exit(-1)

folder = sys.argv[1]
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue

       #convert wav files
       if infilename.endswith('.wav'):
       	sound = AudioSegment.from_wav(infilename)
       	sound = sound.set_channels(2)
       	sound.export(infilename,format="wav")
