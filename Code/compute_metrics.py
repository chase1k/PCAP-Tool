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


def calculate_hop_count():
	pass


def calculate_bytes(list, offset):
	bytes = 0
	for packet in list:
		bytes += int(packet[6]) - offset
	return(bytes)


def compute_node_stats(packets, node_ip):
	# Initalize all the variables
	echo_req_sent = []
	echo_req_recv = []
	echo_reply_sent = []
	echo_reply_recv = []
	
	total_rtt = 0
	total_delay = 0
	hop_count = 0
	
	total_packets = len(packets)

	# increment simple counters
	for packet in packets:
		## DEBUG ##
		# packet = packet[0:12]
		# print(packet)
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

	# Print Simple Stats
	print(f"Echo Requests Sent: {len(echo_req_sent)}")
	print(f"Echo Requests Recived: {len(echo_req_recv)}")
	print(f"Echo Replies Sent: {len(echo_reply_sent)}")	
	print(f"Echo Replies Recieved: {len(echo_reply_recv)}")
	print(f"Echo Requests Bytes Sent: {calculate_bytes(echo_req_sent, 0)}")
	print(f"Echo Requests Bytes Recieved: {calculate_bytes(echo_req_recv, 0)}")
	print(f"Echo Requests Data Sent: {calculate_bytes(echo_req_sent, 42)}")
	print(f"Echo Requests Data Recieved: {calculate_bytes(echo_req_recv, 42)}")
	
	
	# Calcuate Other Stats
	rtt = calculate_rtt(packets, node_ip) # returns (average, total)
	print(f"\nAverage RTT (ms): {rtt[0]:.2f}")
	throughput = calculate_bytes(echo_req_sent, 0) / rtt[1]
	print(f"Echo Request Throughput (kB/sec): {throughput:.1f}")
	goodput = calculate_bytes(echo_req_sent, 42) / rtt[1] 
	print(f"Echo Request Goodput (kB/sec): {goodput:.1f}")
	reply_delay = calculate_reply_delay(packets, node_ip)
	print(f"Average Reply Delay (us): {reply_delay:.2f}")

	# Calculate Hop Count
	print(f"\nAverage Echo Request Hop Count : NULL")
		

# Node Packets contains an array for each node. In that array is an an array of packets.
# Array format : [NODENUMBER, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING]
# Example Data : ['N4', '1444', '1442.007091', '192.168.100.1', '192.168.200.2', 'ICMP', '642', '0x0001', '148/37888', '128', 'Echo (ping) reply', 'request in 1443']
def compute(node_packets) :
	print('called compute function in compute_metrics.py')
	
	# For each node pass in packets and IP of node
	for node in range(0, 1):#len(node_packets)):
		print(f"\nNode {node+1}\n")
		compute_node_stats(node_packets[node], NODE_IPS[node])
	return

