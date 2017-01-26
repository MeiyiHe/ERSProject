from pydub import AudioSegment
from difflib import SequenceMatcher

# Get the voice inputs
var raw_input = ("Please enter the scripts to be processed: ")

words = var.split()

# Concatenate the voice inputs
for word in words
	sound1 = AudioSegment.from_wav(word+".wav")
	sound2 = AudioSegment.from_wav(word+".wav")
	combined_sounds = combined_sound + sound1 + sound2

# Generate the voice outputs
combined_sounds.export("Output.wav", format="wav")


# Output the accuracy
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

print similar(var, )