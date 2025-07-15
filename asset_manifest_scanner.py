# asset_manifest_scanner.py

import os
import hashlib
import argparse
import csv
from datetime import datetime

def sha256_hash(filepath):
    """Calculate SHA256 hash of a file."""
    hash_obj = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def scan_directory(root_path):
    """Scan directory recursively and return list of file metadata."""
    file_data = []
    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            try:
                file_hash = sha256_hash(full_path)
                size = os.path.getsize(full_path)
                modified = datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                file_data.append({
                    'file_path': full_path,
                    'sha256': file_hash,
                    'size_bytes': size,
                    'last_modified': modified,
                })
            except Exception as e:
                print(f"[!] Failed to process: {full_path} ({e})")
    return file_data

def write_manifest(file_data, output_file):
    """Write file data to CSV manifest."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['file_path', 'sha256', 'size_bytes', 'last_modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in file_data:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='File Integrity and Asset Scanner')
    parser.add_argument('directory', help='Target directory to scan')
    parser.add_argument('--output', default='manifest_output.csv', help='Output CSV file')
    args = parser.parse_args()

    print(f"[+] Scanning directory: {args.directory}")
    data = scan_directory(args.directory)
    write_manifest(data, args.output)
    print(f"[✓] Manifest written to: {args.output}")

if __name__ == "__main__":
    main()
