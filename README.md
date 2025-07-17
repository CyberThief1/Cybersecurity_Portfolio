Packet Sniffer (Python + Scapy)


Overview

This project is a basic, professional-grade **packet sniffer** built in Python using the Scapy library. It captures live IP traffic from the local network interface, prints the protocol, source, and destination of each packet to the console, and logs all activity to a CSV file in real time.

Designed as part of my **Cybersecurity Portfolio**, this tool demonstrates core skills in:

- Network protocol inspection (IP/TCP/UDP/ICMP)
- Live traffic capture with Scapy
- File-based logging (CSV format)
- Python scripting for system-level tasks
- PowerShell automation

 What It Does

- Sniffs **live packets** from the local network
- Filters only **IP-level traffic**
- Identifies **protocol type** (TCP, UDP, ICMP)
- Extracts **source and destination IP addresses**
- Timestamps each packet down to the second
- Writes all packet data to `packet_log.csv` in the script directory

 Files

| File               | Description |
|--------------------|-------------|
| `packet_sniffer.py` | Core Python script that handles sniffing and logging |
| `run_sniffer.ps1`   | PowerShell launcher with admin check and log-friendly UI |
| `packet_log.csv`    | Output log file (auto-created on first run) |
| `cheatsheet_snippets.txt` | Reference for `()` vs `[]` in Python syntax |

Requirements

- Python 
- [Scapy]
- [Npcap]  (Windows only)
- Admin privileges (to access the network interface)

Install Scapy:
# powershell
pip install scapy
