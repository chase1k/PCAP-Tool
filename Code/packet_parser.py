import os
# import numpy as np

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
	prefixes = ('No.', '\n')
	# noSections = 0
	# timearray = []
	packetData = []
	# hex = []
	for line in lines[:]:
		if line.startswith(prefixes) or line.__contains__("ICMP"):
			# if line.__contains__('No.'):
			# 	noSections += 1
			if line.__contains__('ICMP'): 
				# timearray.append(line[8:18])
				packetData.append(line)
			# lines.remove(line)
	# for line in lines:
	# 	hexline = line[6:].split('   ', 1)[0].split(' ')
	# 	hex.extend(hexline)
	# hexSep = np.array_split(hex, noSections)
	return packetData

def parse() :
	print('called parse function in packet_parser.py')
	files = opener('Captures')
	# files = ['Captures/example2.txt'] #this is for debug

	nodeArray = []
	nodeNumber = 1
	for file in files: #node
		packetData = hexreader(file)
		packetArray=[]
		for packet in packetData:
			packetDataArray = [("N"+str(nodeNumber))]
			packetDataArray.extend(packet.replace(",", "").split())
			concat1 =  packetDataArray.pop(7) +" "+ packetDataArray.pop(7) +" "+ packetDataArray.pop(7)
			concat2 =  packetDataArray.pop(10) +" "+ packetDataArray.pop(10) +" "+ packetDataArray.pop(10)
			packetDataArray.extend((concat1, concat2))
		# for arr in hexArray: #packet
		# 	#print("node number " + str(nodeNumber) + " packet number " + str(packetNumber+1) + " time recieved: " + str(timearray[packetNumber]))
		# 	sourceAddr = ""
		# 	destinationAddr = ""
		# 	sourceMac = "" #done
		# 	destinationMac = "" #done
		# 	frameLen = 0 #done
		# 	ident = "" #done
		# 	seq = "" #done
		# 	timeToLive = 0 #done
		# 	datLen = 0 #done
			
		# 	#print("array in parse:")
		# 	#print(arr)
		# 	#print(len(arr))
		# 	packetDataArray = [("N"+str(nodeNumber)),("P" + str(packetNumber+1)), (timearray[packetNumber])]
			
		# 	#array hell
		# 	sourceAddr
		# 	destinationAddr
		# 	destinationMac = str(arr[0]) + ":" + str(arr[1]) + ":" + str(arr[2]) + ":" + str(arr[3]) + ":" + str(arr[4]) + ":" + str(arr[5])
		# 	sourceMac = str(arr[6]) + ":" + str(arr[7]) + ":" + str(arr[8]) + ":" + str(arr[9]) + ":" + str(arr[10]) + ":" + str(arr[11])
		# 	#ignore index 12, 13 (type, we already know this is all IPv4)
		# 	#ignore index 14 (header length)
		# 	#ignore index 15 (diff services field)
		# 	datLen = int(arr[16], 16) + int(arr[17], 16)
		# 	frameLen = len(arr)
		# 	ident =  "0x" + str(arr[18]) + str(arr[19])
		# 	#ignore index 20, 21 (frame offset delimiter)
		# 	timeToLive = int(arr[22], 16) + int(arr[23], 16)
		# 	#ignore index 24 (protocol, we already know its ICMP)
		# 	seq = str(int((arr[40]+arr[41]),16))+"/"+str(int((arr[41]+arr[40]),16))
		# 	packetNumber+=1
		# 	packetDataArray.extend((sourceAddr, destinationAddr, sourceMac, destinationMac, "ICMP", frameLen, ident, seq, timeToLive, datLen))
			packetArray.append(packetDataArray)
		nodeNumber += 1
		
		nodeArray.append(packetArray)
	print(nodeArray)
	return(nodeArray) #array formatted 'NODENUMBER, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING'


	