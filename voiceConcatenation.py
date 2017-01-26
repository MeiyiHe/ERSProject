from pydub import AudioSegment

#ask for the two voice files
file_1 = raw_input("Please enter the first voice file")
file_2 = raw_input("Please enter the second voice file")

sound_1 = AudioSegment.from_wav("/path/to/"+file_1+".wav")
sound_2 = AudioSegment.from_wav("/path/to"+file_2+".wav")

combined = sound_1+sound_2
combined.export("", format="wav")