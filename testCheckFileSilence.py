import struct
import wave
import pyaudio
import sys
import os
from pydub import AudioSegment

CHUNK = 1024

from pydub import AudioSegment
from pydub.silence import split_on_silence

sound = AudioSegment.from_mp3("sounds/CatScaredDogRed.mp3")
chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len=150,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-40
)
a = []
for i, chunk in enumerate(chunks):
    chunk.export("sounds/testChunks/chunk{0}.wav".format(i), format="wav")
for i, chunk in enumerate(chunks):
	a.append((os.path.getsize("sounds/testChunks/chunk{0}.wav".format(i)),i))


print "before sorted "
print a 

sorted_a = sorted(a, key= lambda x:x[0])
print "after sorted "
print sorted_a


