# Use speech recognizer to get the text of audio segments
from sys import argv
import speech_recognition as sr
import os

#usage: python googleScript.py testWrite.txt

script, filename = argv

print "We're going to write on%r." % filename

print "Opening the file..."
target = open(filename, 'w')


unrelated_paths = ['..', './SmallSnippets']
chunk_files = (os.path.join(p, o) for p in unrelated_paths
              for o in os.listdir(p)
              if (o.lower().endswith('.wav')
                  and os.path.isfile(os.path.join(p, o))))
# use the audio file as the audio source

r = sr.Recognizer()
for chunk_file in chunk_files:
    print chunk_file
    with sr.AudioFile(chunk_file) as source:
    	audio = r.record(source) # read the entire audio file
	try:
		#print("Google thinks you said " + r.recognize_google(audio))
		target.write(r.recognize_google(audio))
		target.write("\n")
	except sr.UnknownValueError:
		target.write("ERROR")
	except sr.RequestError as e:
	    target.write("Google error; {0}".format(e))
