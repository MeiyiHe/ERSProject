#split the wav file to chunks by several time points(in miliseconds and sequential order)
#python3 SplitOnTime.py filename.wav outputDir time1 time2 ... timeN
import sys, os
from pydub import AudioSegment

#check the command line input
if len(sys.argv) < 4:
	print("Split the wav file to chunks by several time points."
	+ "\n\nUsage: %s filename.wav outputDir time1 time2 ... timeN\n" % sys.argv[0])
	sys.exit(-1)

filename = sys.argv[1]
outputDir = sys.argv[2]
print("Spliting the file - "+filename)
if filename.endswith(".wav"):
	audio = AudioSegment.from_wav(filename)
else:
	print("The inputfile should be a wav file!")
	sys.exit(-1)

if not os.path.isdir(outputDir):
	print("The output is not a directory!")
	sys.exsit(-1)

previousT = 0
total_time = audio.duration_seconds * 1000
for i in range(len(sys.argv)):
	#skip the first three items(not the time points)
	if i==0 or i==1 or i==2:
		continue

	time = float(sys.argv[i])
	print time
	if time > total_time: #check if the time point is valid
		print("The duration of the voice file is " + str(total_time))
		print("At least one of the time points is not valid!")
		break

	#export the file
	export_a = audio[previousT:time]
	chunk_name = "from{0}to{1}.wav".format(int(previousT),int(time))
	previousT = time
	print("exporting..."+chunk_name)
	export_a.export(outputDir+"/"+chunk_name, format="wav")

	#export the remaining part
	if i== len(sys.argv)-1 :
		export_a = audio[previousT:total_time]
		chunk_name = "from{0}to{1}.wav".format(int(previousT),int(total_time))
		print("exporting..."+chunk_name)
		export_a.export(outputDir+"/"+chunk_name, format="wav")


print("Finished!")
