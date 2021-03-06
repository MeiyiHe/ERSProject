import struct
import wave
import pyaudio
import sys
import os
from pydub import AudioSegment

CHUNK = 1024

from pydub import AudioSegment
from pydub.silence import split_on_silence

sound = AudioSegment.from_mp3("./CatScaredDogRed.mp3")
chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len=150,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-40
)

# store the splitted voice files into chunks and store it into a[]
a = []
for i, chunk in enumerate(chunks):
    chunk.export("./splittedAudioFiles/chunk{0}.wav".format(i), format="wav")

for i, chunk in enumerate(chunks):
	a.append((os.path.getsize("./splittedAudioFiles/chunk{0}.wav".format(i)),i))


# check how many elements in the array a 
bfLen = len(a)


print "before sorted "
print a 


# sorted_a[] will store the chunk in an ascending file size order
sorted_a = sorted(a, key = lambda x:x[0])
print "after sorted "
print sorted_a


# remove the empty file from sorted[] by check the difference between expected word numbers 
# and the actual word numbers
indexToRemove = []
for j in range(0,5):
	indexToRemove.append(sorted_a[j][1])
	print sorted_a[j][1]

	os.remove("./splittedAudioFiles/chunk{0}.wav".format(indexToRemove[j]))











