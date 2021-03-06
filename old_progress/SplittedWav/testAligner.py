from pydub import AudioSegment
from difflib import SequenceMatcher
import speech_recognition as sr
from os import path
import os

# Get the voice inputs
var = raw_input("Please enter the scripts to be processed: ")

input_file = open(var,'rb')
inputs = input_file.read()
words = inputs.split()

combined_sounds = AudioSegment.from_file(words[0]+".wav")

# Concatenate the voice inputs
for i in range(len(words)):
	if i==0 :
		continue
	new_sound_file = AudioSegment.from_file(words[i] + ".wav")
	combined_sounds=combined_sounds+new_sound_file

# Generate the voice outputs
combined_sounds.export("Output.wav", format="wav")

'''
# obtain path to "english.wav" in the same folder as this script
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "Output.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    combined = r.recognize_google(audio)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
'''
print inputs

#print combined
# Output the accuracy
#iprint SequenceMatcher(None, inputs, combined).ratio()
