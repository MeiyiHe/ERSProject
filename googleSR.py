# Use speech recoginizer to get the text of audio segment
import speech_recognition as sr
import os


unrelated_paths = ['..', './splittedAudioFiles']
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
		print("Sphinx thinks you said " + r.recognize_google(audio))
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
	    print("Sphinx error; {0}".format(e))





