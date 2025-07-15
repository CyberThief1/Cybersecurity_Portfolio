# 🛡 Asset Recurse Scanner

**Author:** CyberThief1  
**Project Path:** `C:\Users\imbri\OneDrive\Desktop\Cybersecurity_Portfolio\Asset_Recurse_scanner`  
**Purpose:** File integrity & asset inventory snapshot for cybersecurity operations

---

##  What It Does

The `asset_inventory.py` script recursively scans a target directory, computes a **SHA256 hash** for every file, and saves the output into a structured CSV file.

It is designed for use in:

- Cybersecurity audits
- Integrity checks
- Forensic investigations
- File inventorying in secure environments

---

##  Output

A file called `asset_inventory.csv` will be written directly into the folder containing the script. It includes:

| full_path                           | filename              | sha256                                |
|------------------------------------|------------------------|----------------------------------------|
| `C:\example\folder\file.txt`       | `file.txt`             | `3a1fcd97...`                           |

---

##  How to Use

###  Option 1: Direct Run

```powershell
python asset_inventory.py --target "C:\Path\To\Folder"

