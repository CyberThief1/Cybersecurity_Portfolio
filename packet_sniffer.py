import csv
import os
from datetime import datetime
from scapy.all import sniff,IP, TCP, UDP, ICMP

LOG_FILE = os.path.join(os.path.dirname(__file__), "packet_log.csv")

# Write header if file doesn't exist yet
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Protocol", "Source IP", "Destination IP"])
                        
def process_packet(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        proto = None

        if packet.haslayer(TCP):
            proto = "TCP"
        elif packet.haslayer(UDP):
            proto = "UDP"
        elif packet.haslayer(ICMP):
            proto = "ICMP"
        else:
            proto = ip_layer.proto

        src = ip_layer.src
        dst = ip_layer.dst
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] {proto} Packet | Source: {src} -> Destination: {dst}")

        with open(LOG_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, proto, src, dst])


if __name__ == "__main__":
  print("[*] Starting packet sniffer... Press Ctrl+C to stop.\n")
  sniff(filter="ip", prn=process_packet, store=False)
