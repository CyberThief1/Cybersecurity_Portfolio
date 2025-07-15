# asset_inventory.py

import os
import argparse
import hashlib
import csv

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"[ERROR] {e}"

def scan_directory(target_dir):
    inventory = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            sha256_hash = calculate_sha256(full_path)
            inventory.append({
                'full_path': full_path,
                'filename': file,
                'sha256': sha256_hash
            })
    return inventory

def write_to_csv(data, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['full_path', 'filename', 'sha256'])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asset Inventory Scanner")
    parser.add_argument('--target', type=str, default=os.getcwd(),
                        help="Target directory to scan (default: current directory)")
    args = parser.parse_args()

    print(f"[+] Scanning directory: {args.target}")
    results = scan_directory(args.target)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_output = os.path.join(script_dir, 'asset_inventory.csv')
    write_to_csv(results, csv_output)
    print(f"[✓] Inventory written to: {csv_output}")
