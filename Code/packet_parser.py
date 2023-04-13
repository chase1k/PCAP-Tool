import os
import numpy as np

def opener(directory):
	fileArray = []
	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if os.path.isfile(f) and f.find('ICMP_Node')!=-1:
			fileArray.append(f)
	return(fileArray)

def hexreader(file):
	print('filename: ' + file)
	node = open(file, 'r')
	lines = node.readlines()
	
	prefixes = ('No.', '    ', '\n')
	sep = '   ' 
	noSections = 0
	timearray = []
	hex = []
	for line in lines[:]:
		if line.startswith(prefixes):
			lines.remove(line)
			if line.startswith('No.'):
				noSections += 1
			if line.startswith('    '):
				timearray.append(line[8:17])
	for line in lines:
		hex.append(line[6:].split(sep, 1)[0])
	hexSep = np.array_split(hex, noSections)
	return hexSep, timearray

def parse() :
	print('called parse function in packet_parser.py')
	#files = opener('Captures')
	files = ['Captures/example.txt'] #this is for debug
	for file in files: #node
		hexArray, timearray = hexreader(file)
		
		packetNumber = 1
		time = ""
		sourceAddr = ""
		destinationAddr = ""
		protocol = "ICMP"
		frameLen = 0
		type = ""
		ID = ""
		seqNum = ""
		TTL = 0

		for arr in hexArray:
			print("packet number " + str(packetNumber) + " time recieved: " + str(timearray[packetNumber-1]))
			for line in arr:
				bytes = line.split(' ')
				print(bytes)
			packetNumber+=1

parse()

# destinationMac = ""
# sourceMac = ""
# sourcePort = ""
# destinationPort = ""


	