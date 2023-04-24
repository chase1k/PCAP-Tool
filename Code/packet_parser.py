import os
import numpy as np

def opener(directory):
	fileArray = []
	for filename in os.listdir(directory):
		f = os.path.join(directory, filename) # get the directory all sorted out
		if os.path.isfile(f) and f.find('ICMP_Node')!=-1: # find files with the right name
			fileArray.append(f) # add them to the list of files to read
	return fileArray

def reader(file):
	print('filename: ' + file)
	node = open(file, 'r')
	lines = node.readlines()
	prefixes = ('No.', '\n') # prefixes for lines to void
	packetData = []
	hexArraytmp = [] # temp array to store all of the hex data at once
	hexSections = 0 # how many sections to segment the temp array into
	for line in lines[:]:
		if "ICMP" in line:
			packetData.append(line)
			lines.remove(line) # remove lines after parsing data
			hexSections += 1 # number of sections the temp array should be split into
		if line.startswith(prefixes):
			lines.remove(line) # remove extraneous lines
	for line in lines:
		hex = line[6:].split('   ', 1)[0].split(' ') # get rid of prefix and suffix on the hex and split into an array
		hexArraytmp.extend(hex)
	hexArray = np.array_split(hexArraytmp, hexSections) #split the hex into chunks
	return packetData, hexArray

def parse() :
	print('called parse function in packet_parser.py')
	files = opener('Captures')
	files.sort(reverse=True) #reverse order the files (does not have to be reverse)
	nodeArray = [] # array of nodes
	nodeNumber = 1
	for file in files: # per node operations
		packetData, hexArray = reader(file)
		packetArray=[] # array of packets to be output
		packetnum = 0 # keep count of packets to associate the hex to the packet data
		for packet in packetData:
			packetDataArray = [("N"+str(nodeNumber))]
			packetDataArray.extend(packet.replace(",", "").replace("ttl=", "").replace("id=", "").replace("seq=", "").split()) # format
			concat1 =  packetDataArray.pop(7) +" "+ packetDataArray.pop(7) +" "+ packetDataArray.pop(7) # fix the data parts that were split on spaces when they were not supposed to be
			concat2 =  packetDataArray.pop(10).strip("(") +" "+ packetDataArray.pop(10) +" "+ packetDataArray.pop(10).strip(")") # fix the data parts that were split on spaces when they were not supposed to be
			packetDataArray.extend((concat1, concat2)) # add back fixed data
			packetDataArray.extend([hexArray[packetnum]]) #tacks the HEX onto the end as a numpy array
			packetArray.append(packetDataArray) # append it all to the return (2d)
			packetnum += 1
		nodeNumber += 1
		nodeArray.append(packetArray) # append it all to the final return  (3d)
	# print(nodeArray) #for debug
	return(nodeArray) #array formatted [[[NODENUMBER 1, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING, [RAW HEX DATA]][...]][[2...][...]][[...][...]]] (its a 3d* array separated in to node groups where each node group is full of arrays the correspond to packets, the asterisk is because with the HEX data added its technically a 4D array)