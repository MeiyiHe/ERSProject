
import struct
import wave
import pyaudio
import sys
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

sound = AudioSegment.from_mp3("/Users/Siya/Documents/UCSD/ERSP/AudioSource/TestAudio2.MP3")
chunks = split_on_silence(sound, 
    # must be silent for at least half a second(>=500)
    min_silence_len=1200,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-40
)
for i, chunk in enumerate(chunks):
    out_file = "/Users/Siya/Documents/UCSD/ERSP/AudioSource/AfterSplit/chunk{0}.wav".format(i)
    print "exporting", out_file
    chunk.export(out_file, format="wav")



