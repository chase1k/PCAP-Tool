from filter_packets import *
from packet_parser import *
from compute_metrics import *

filter()
node_packets = parse()
compute(node_packets)
