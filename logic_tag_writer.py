# logic_tag_writer.py

import os
import hashlib
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading

CACHE_FILE = "tagging_manifest.csv"
SUPPORTED_EXTENSIONS = [".txt"]
LOCK = threading.Lock()

# Define rule-based keyword tag map
KEYWORD_TAGS = {
    "ransomware": ["ransomware", "encryption", "file-locking"],
    "c2": ["command-control", "callback", "beacon"],
    "exfil": ["data-exfiltration", "exfil"],
    "persistence": ["startup-injection", "registry-hook", "autorun"],
    "lateral": ["lateral-movement", "pivoting"],
    "dns": ["dns-tunneling", "covert-channel"],
    "phishing": ["email-attack", "credential-theft"],
    "powershell": ["scripted-attack", "living-off-land"],
    "mimikatz": ["credential-dumping", "memory-extraction"],
}

def sha256_hash(filepath):
    """Calculate SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def already_processed(file_hash):
    """Check if hash exists in cache."""
    if not os.path.exists(CACHE_FILE):
        return False
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return any(file_hash in line for line in f)

def append_to_cache(file_hash, filepath):
    """Append hash to manifest cache."""
    with LOCK:
        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(f"{file_hash},{filepath}\n")

def classify_text(content):
    """Apply keyword rules to content and return logic tags."""
    tags_found = set()
    for keyword, tags in KEYWORD_TAGS.items():
        if keyword.lower() in content.lower():
            tags_found.update(tags)

    if not tags_found:
        tags_found.add("unclassified")

    return sorted(tags_found)

def write_tag_file(original_path, tags):
    """Write the tag file next to the source file."""
    tag_path = Path(f"{original_path}.tag.txt")
    with open(tag_path, "w", encoding="utf-8") as f:
        f.write(f"[LOGIC_TAGS]: {', '.join(tags)}\n")
        f.write("[FUNCTION]: static-rule-classifier\n")
        f.write("[CONNECTION_SCOPE]: local\n")

def process_file(file_path):
    try:
        file_hash = sha256_hash(file_path)
        if already_processed(file_hash):
            print(f"[=] Skipped (cached): {file_path}")
            return

        print(f"[+] Tagging: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tags = classify_text(content)
        write_tag_file(file_path, tags)
        append_to_cache(file_hash, file_path)

    except Exception as e:
        print(f"[!] Error processing {file_path}: {e}")

def scan_and_tag(directory):
    """Walk the directory and process all text files."""
    all_files = []
    for root, _, files in os.walk(directory):
        for name in files:
            if Path(name).suffix.lower() in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, name)
                all_files.append(full_path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file, all_files)

def main():
    parser = argparse.ArgumentParser(description="Static logic tagger (non-AI)")
    parser.add_argument("directory", help="Folder of .txt files to tag")
    args = parser.parse_args()

    print(f"[+] Scanning folder: {args.directory}")
    scan_and_tag(args.directory)
    print("[✓] Tagging complete.")

if __name__ == "__main__":
    main()
