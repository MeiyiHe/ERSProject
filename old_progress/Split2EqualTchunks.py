#split to equal time chunks
from pydub import AudioSegment
from pydub.utils import make_chunks
import sys

myaudio = AudioSegment.from_file("1112" , "wav") 
chunk_length_ms = 10000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print "exporting", chunk_name
    chunk.export(chunk_name, format="wav")