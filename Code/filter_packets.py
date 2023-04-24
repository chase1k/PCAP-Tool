def filter():
	print('called filter function in filter_packets.py')

	filename = '../Captures/Node1.txt'
	file = open(filename,'r')
	line = file.readline()
	newFile = open('../Captures/ICMP_Node1.txt','w')
	filta(file, newFile, line)

	filename = '../Captures/Node2.txt'
	file = open(filename,'r')
	line = file.readline()
	newFile = open('../Captures/ICMP_Node2.txt','w')
	filta(file, newFile, line)

	filename = '../Captures/Node3.txt'
	file = open(filename,'r')
	line = file.readline()
	newFile = open('../Captures/ICMP_Node3.txt','w')
	filta(file, newFile, line)

	filename = '../Captures/Node4.txt'
	file = open(filename,'r')
	line = file.readline()
	newFile = open('../Captures/ICMP_Node4.txt','w')
	filta(file, newFile, line)

def filta(file, newFile, line):

	while line:
		if 'Echo' in line:
			newFile.write("No.     Time           Source                Destination           Protocol Length Info\n")

			while line:

				# print(line)
				newFile.write(line)
				line = file.readline()	

				if line.__contains__('No.'):
					line = None
					exit

			exit
		line = file.readline()
	file.close()
	newFile.close()
    