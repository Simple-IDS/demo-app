###TCP CONNECTION DETECTOR###
from scapy.all import *
import time
from collections import defaultdict
interval = 30
threshold = 100
syn_packets = defaultdict(list)

def analysis(packet):
    if not packet.haslayer(TCP):
        return
    
    src = packet[IP].src
    dst = packet[IP].dst
    tcp = packet[TCP]
    if tcp.flags == 'S':
        syn_packets[(src, dst)].append(time.time())
        syns = [t for t in syn_packets[(src, dst)] if time.time() - t < interval]
        syn_packets[(src, dst)] = syns
        if len(syns) > threshold:
            print(f"Potential port scanning detected from {src} to {dst}. SYN count: {len(syns)}")
            print(f"{len(syns)} SYN packets in the last {interval} seconds.")
            syn_packets[(src, dst)] = []
            
def main():
    print("Starting TCP connection detector...")
    try:
        sniff(filter="tcp", prn=analysis, store=0)
    except Exception as e:
        print(f"Stopping TCP connection detector... Error: {e}")
def periodically():
    print("Periodic check running...")
    main()
    print("Periodic check completed.")
        
if __name__ == "__main__":
    periodically()
    time.sleep(20)
    