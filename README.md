\# Asset Integrity Monitor



\*\*Asset Integrity Monitor\*\* is a file integrity and asset discovery tool written in Python and executed via PowerShell. It recursively scans a target directory, computes SHA256 hashes for all files, and generates a structured `.csv` manifest.



This project is designed for security engineers, systems administrators, and incident response professionals who need a lightweight tool for asset baselining, file inventory, or unauthorized change detection.



---



\## Features



\- Recursive directory scan

\- SHA256 hash generation for tamper detection

\- CSV output including file path, size, and last modified timestamp

\- PowerShell launcher for ease of use and automation

\- Fully portable and free of third-party dependencies



---



\## File Overview



| File                         | Description                                 |

|------------------------------|---------------------------------------------|

| `asset\_manifest\_scanner.py`  | Python script that handles scanning and hashing |

| `run\_asset\_scan.ps1`         | PowerShell wrapper to launch the scan       |

| `requirements.txt`           | (Optional) Python requirements list         |

| `manifest\_output\_example.csv`| Example output of a completed scan          |



---



\## Usage



\### Option 1: Run via PowerShell (preferred for automation)



```powershell

.\\run\_asset\_scan.ps1 -TargetDirectory "C:\\Path\\To\\Scan" -OutputFile "scan\_manifest.csv"



