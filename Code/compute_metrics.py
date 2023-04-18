NODE_IPS = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]

def compute_node_stats(packets, node_ip):
	# Initalize all the variables
	req_sent = 0
	req_recv = 0
	rep_sent = 0
	rep_recv = 0 
	req_byte_sent = 0
	req_byte_recv = 0
	rep_byte_sent = 0
	rep_byte_recv = 0
	
	total_rtt = 0
	total_delay = 0
	hop_count = 0
	
	total_packets = len(packets)

	# organize packets and increment counters
	for packet in packets:
		# Node Sent
		if packet[3] == node_ip:
			pass	

		# Node Recieved
		if packet[4] == node_ip:
			pass
		
		# Error
		else:
			print(f"Node IP mismatch : Packet # : {packet[1]}, Node # : {packet[0]}")

		# Calcuate Other Stats
		

# Node Packets contains an array for each node. In that array is an an array of packets.
# Array format : [NODENUMBER, PACKETNUMBER, TIME, SRC, DEST, PROTOCOL, LEN, ID, SEQNUM(LE/BE), TTL, TYPE, PAIRING]
# Example Data : ['N4', '1444', '1442.007091', '192.168.100.1', '192.168.200.2', 'ICMP', '642', '0x0001', '148/37888', '128', 'Echo (ping) reply', 'request in 1443']
def compute(node_packets) :
	print('called compute function in compute_metrics.py')
	
	# For each node pass in packets and IP of node
	for node in range(0, len(node_packets)):
		compute_node_stats(node_packets[node], NODE_IPS[node])
	return

