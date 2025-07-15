# Secure Log Collector

This project is a two-part Python-based utility designed to securely collect and show Windows Event Logs. It was intended for use in cybersecurity environments where log integrity, tamper resistance, and secure archives are important — such as incident response, threat analysis, and forensic investigation. (audits)

I developed this tool to demonstrate competency in basic system forensics, file handling, encryption practices, and scripting on Windows systems. (powershell, bash, Admin runs.) The goal was to create something that could be operationally useful, not just theoretical.

---
## Project Overview

The toolset is divided into two main scripts:

### 1. `secure_log_collector.py`

This script collects logs from key Windows Event Viewer sources (`System`, `Security`, and `Application`) using the built-in `wevtutil` command. It performs the following actions:

- Exports the logs as `.evtx` files with unique timestamps
- Saves the output to a local `logs/` directory
- Compresses the collected logs into a single `.zip` archive
- Generates a SHA256 hash of the `.zip` file and saves it in a `.sha256.txt` file alongside the archive

This hashing step provides tamper-evident verification. Any change to the archived logs will produce a different hash, which can be used to detect unauthorized alterations.

**Note:** Exporting the `Security` event log requires administrative privileges. If running from PowerShell, the shell must be launched as Administrator.

---

### 2. `encrypted_log_collector.py`

This script encrypts the `.zip` archive using symmetric encryption (Fernet, based on AES-128). It prompts the user for:

- The path to the `.zip` file created by the previous script
- A password to derive a cryptographic key

It outputs:
- An encrypted version of the archive (`.zip.encrypted`)
- A text file containing a SHA256 hash of the derived key (for optional later verification)

The purpose of this script is to securely store or transmit collected logs without risking exposure. The encryption is designed to ensure confidentiality in environments where sensitive event logs must be preserved or reviewed later. The two could be merged for maximum efficiency and possibly use a .csv for userfriendly interactions and forensics, but I did it this way to show two separate instances.

---

## Tools & Technologies

- Python 3
- PowerShell (used for launching the scripts on Windows)
- Standard Python libraries: `os`, `hashlib`, `subprocess`, `datetime`, `zipfile`
- External Python library: `cryptography` (for Fernet encryption)
- Windows utility: `wevtutil` (for event log export)

---

## How to Use

### Requirements

- Python 3.8+
- PowerShell (on Windows)
- Admin rights (required for full log access)

### Installation

1. Clone the repository or download the project files.
2. Install the required Python package:

```bash
pip install cryptography

