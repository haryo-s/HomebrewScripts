import csv
import os

# Initialising variables
ItemExtensions = '.mp4', '.avi', '.mkv' # List of possible video formats 
ScriptPath = os.path.dirname(os.path.realpath(__file__)) # Current location of script
#TargetDirectory = ScriptPath + '\Videos' # Designates directory to scan. Needs to be changed for production
TargetDirectory = r'\\HARYONAS\media\video'
TargetDirectoryfsencode = os.fsencode(TargetDirectory)
ffprobeArguments = " -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 " # FFProbe arguments to output only the codec

# Initialises and creates a new .csv, setting up basic parameters to work with it
with open('output.csv', 'w') as csvfile: 
	header = ['Filename', 'Item location', 'Codec']
	csvOutput = csv.DictWriter(csvfile, fieldnames=header, lineterminator='\n', delimiter=',')
	csvOutput.writeheader()

	# Go through every file in folder
	for root, dirs, files in os.walk(TargetDirectory):
		for item in files:
			if item.endswith(ItemExtensions):
				locationItem = os.path.join(root, item) 
				returnedCodec = os.popen("ffprobe" + ffprobeArguments + '\"' + locationItem + '\"').read()
		
				#print("\n")
				print(locationItem)
				print(returnedCodec)
			
				csvOutput.writerow({'Filename': item, 'Item location': locationItem, 'Codec': returnedCodec}) 
		
			else: # If file does not end in a video format, throw error and does not add it to the list.
				print("Error!")
				print(os.path.join(root, item) + " does not end in " + ', '.join(ItemExtensions))
				print("\n")
		
		