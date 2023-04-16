import os

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
	packetData = []
	for line in lines[:]:
		if "ICMP" in line:
			packetData.append(line)
	return packetData

def parse() :
	print('called parse function in packet_parser.py')
	files = opener('Captures')
	nodeArray = []
	nodeNumber = 1
	for file in files: #node
		packetData = hexreader(file)
		packetArray=[]
		for packet in packetData:
			packetDataArray = [("N"+str(nodeNumber))]
			packetDataArray.extend(packet.replace(",", "").replace("ttl=", "").replace("id=", "").replace("seq=", "").split())
			concat1 =  packetDataArray.pop(7) +" "+ packetDataArray.pop(7) +" "+ packetDataArray.pop(7)
			concat2 =  packetDataArray.pop(10).strip("(") +" "+ packetDataArray.pop(10) +" "+ packetDataArray.pop(10).strip(")")
			packetDataArray.extend((concat1, concat2))
			packetArray.append(packetDataArray)
		nodeNumber += 1
		nodeArray.append(packetArray)
	print(nodeArray)
	return(nodeArray) #array formatted 'NODENUMBER, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING'
parse() #for debug	