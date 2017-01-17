"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
from pydub import AudioSegment
CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)
#w1 = wave.open("cow2.wav", "rb")


#splitting audio into multiple pieces
# sound = AudioSegment.from_mp3("161112_001.mp3")
# sound.export("./1112", format="wav")

w1 = wave.open("chunk0.wav", "rb")

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(w1.getsampwidth()),
                channels=w1.getnchannels(),
                rate=w1.getframerate(),
                output=True)

data1 = w1.readframes(CHUNK)


while data1 != '':
    stream.write(data1)
    data1 = w1.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()