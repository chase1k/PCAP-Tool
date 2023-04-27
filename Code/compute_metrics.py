import csv

# Hardcode the IPs
NODE_IPS = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]


def calculate_rtt(list, node_ip):
	total_delay = 0
	ping_count = 0
	for i in range(0, len(list)):
		packet = list[i][0:12]
		if 'request' in packet[10] and packet[3] == node_ip:
			reply_id = int(packet[11].split(' ')[2])
			
			# Search forward until ID is found
			for reply_i in range(i, len(list)):
				reply_packet = list[reply_i][0:12]
				if int(reply_packet[1]) == reply_id:
					break
				else:
					continue
			
			# Calculate delay
			delta = float(reply_packet[2]) - float(packet[2])
			total_delay += delta*1000 # Make into ms
			ping_count += 1

	average_delay = (total_delay/ping_count)
	return(average_delay,total_delay)


def calculate_reply_delay(list, node_ip):
	total_delay = 0
	count = 0
	for i in range(0, len(list)):
		packet = list[i][0:12]
		if 'reply' in packet[10] and packet[3] == node_ip:
			request_id = int(packet[11].split(' ')[2])
			
			# Search backward until ID is found
			for request_i in range(i, 0, -1):
				request_packet = list[request_i][0:12]
				if int(request_packet[1]) == request_id:
					break
				else:
					continue
			
			# Calculate delay
			delta = float(packet[2]) - float(request_packet[2])
			total_delay += delta*1000000 # Make into us
			count += 1
		
	average_delay = (total_delay/count)
	return(average_delay)


def calculate_hop_count(packets):
	hops = 0
	count = 0
	for packet in packets:
		hops += abs(int(packet[9]) - 129) # We find the hops with a little subtraction magic, we know ttl is 128 by default
		count += 1
	average_hop = hops/count
	return(average_hop)

def calculate_bytes(list, offset):
	bytes = 0
	for packet in list:
		bytes += int(packet[6]) - offset
	return(bytes)


def compute_node_stats(packets, node_ip, f):
	# Initalize all the variables
	echo_req_sent = []
	echo_req_recv = []
	echo_reply_sent = []
	echo_reply_recv = []
	hop_count = 0

	## Sort Packets ##
	for packet in packets:
		## Node Sent ##
		if packet[3] == node_ip:
			if 'reply' in packet[10]:
				echo_reply_sent.append(packet)
				# data is len + 14
			if 'request' in packet[10]:
				echo_req_sent.append(packet)
		## Node Recieved ##
		elif packet[4] == node_ip:
			if 'reply' in packet[10]:
				echo_reply_recv.append(packet)
			if 'request' in packet[10]:
				echo_req_recv.append(packet)
		# Error
		else:
			print(f"Node IP mismatch : Packet # : {packet[1]}, Node # : {packet[0]}, SRC IP : {packet[3]}, DST IP : {packet[4]}")

	### Calculate & Write Stats ###

	# Basic stats
	f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\r\n")
	total_req_sent = len(echo_req_sent)
	total_reply_sent = len(echo_reply_sent)
	total_req_recv = len(echo_req_recv)
	total_reply_recv = len(echo_reply_recv)
	f.write(f"{total_req_sent},{total_reply_sent},{total_req_recv},{total_reply_recv}\r\n")

	f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\r\n")
	request_bytes_sent = calculate_bytes(echo_req_sent, 0)
	request_data_sent = calculate_bytes(echo_req_sent, 42)
	f.write(f"{request_bytes_sent},{request_data_sent}\r\n")
	
	f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\r\n")
	request_bytes_received = calculate_bytes(echo_req_recv, 0)
	request_data_received = calculate_bytes(echo_req_recv, 42)
	f.write(f"{request_bytes_received},{request_data_received}\r\n")
	
	
	# Calcuate Other Stats
	rtt = calculate_rtt(packets, node_ip) # returns (average, total)
	throughput = calculate_bytes(echo_req_sent, 0) / rtt[1]
	goodput = calculate_bytes(echo_req_sent, 42) / rtt[1] 
	reply_delay = calculate_reply_delay(packets, node_ip)
	hop_count = calculate_hop_count(echo_reply_recv)

	f.write(f"\r\nAverage RTT (milliseconds),{rtt[0]:.2f}\r\n")
	f.write(f"Echo Request Throughput (kB/sec),{throughput:.1f}\r\n")
	f.write(f"Echo Request Goodput (kB/sec),{goodput:.1f}\r\n")
	f.write(f"Average Reply Delay (microseconds),{reply_delay:.2f}\r\n")
	f.write(f"Average Echo Request Hop Count,{hop_count:.2f}\r\n\r\n")

	# Print one packet to show hex is being parsed
	# See "packet_parser.py" for more details
	if node_ip == NODE_IPS[3]:
		print(f"Example Packet for Hex Parsing : {packets[0]}")	
		

# Node Packets contains an array for each node. In that array is an an array of packets.
# Array format : [NODENUMBER, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING]
# Example Data : ['N4', '1444', '1442.007091', '192.168.100.1', '192.168.200.2', 'ICMP', '642', '0x0001', '148/37888', '128', 'Echo (ping) reply', 'request in 1443']
def compute(node_packets) :

	# Open File
	f = open("metrics.csv", "w")
	# For each node pass in packets and IP of node
	for node in range(0, len(node_packets)):
		f.write(f"Node {node+1}\r\n\r\n")
		compute_node_stats(node_packets[node], NODE_IPS[node], f)
	f.close()
	print("Metrics written to \"metrics.csv\"")
	return

	

