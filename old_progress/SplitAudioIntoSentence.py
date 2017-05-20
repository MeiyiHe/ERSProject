# Chop up a long audio into small audio segments containing 1 to 4 words
import struct
import wave
import pyaudio
import sys
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

#average_loudness = podcast.rms


sound = AudioSegment.from_mp3("/Users/meiyihe/Desktop/testSOS/170203_004.MP3")
average_loudness = sound.rms
#silence_threshold = average_loudness * db_to_float(-30)

chunks = split_on_silence(sound, 
    # must be silent for at least half a second(>=1200)
    min_silence_len=275,

    # consider it silent if quieter than -40 dBFS
    silence_thresh=-40
)
for i, chunk in enumerate(chunks):
    out_file = "/Users/meiyihe/Desktop/testSOS/outChunks4/chunk{0}.wav".format(i)
    print "exporting", out_file
    chunk.export(out_file, format="wav")



