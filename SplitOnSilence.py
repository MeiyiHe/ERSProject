# Chop up a long audio into small audio segments containing 1 to 4 words
import struct
import wave
import pyaudio
import sys
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

sound = AudioSegment.from_mp3("./TestAudio2.MP3")
chunks = split_on_silence(sound, 
    # must be silent for at least half a second(>=1200)
    min_silence_len=1200,

    # consider it silent if quieter than -40 dBFS
    silence_thresh=-40
)
for i, chunk in enumerate(chunks):
    out_file = "./chunk{0}.wav".format(i)
    print "exporting", out_file
    chunk.export(out_file, format="wav")



