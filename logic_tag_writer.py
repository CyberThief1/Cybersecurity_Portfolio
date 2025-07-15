# logic_tag_writer.py

import os
import hashlib
import threading
import openai
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

CACHE_FILE = "tagging_manifest.csv"
SUPPORTED_EXTENSIONS = [".txt"]
LOCK = threading.Lock()

def sha256_hash(filepath):
    """Calculate the SHA256 hash of a file."""
    hash_obj = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def already_processed(file_hash):
    """Check if file hash is already in the manifest cache."""
    if not os.path.exists(CACHE_FILE):
        return False
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return any(file_hash in line for line in f)

def append_to_cache(file_hash, filepath):
    """Record processed file hash + path to manifest."""
    with LOCK:
        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(f"{file_hash},{filepath}\n")

def generate_tags(file_path):
    """Send file content to GPT and extract tags."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = (
        "You are an AI semantic classifier.\n"
        "Given the content of this file, return logic tags that describe it.\n"
        "Use this format:\n"
        "[LOGIC_TAGS]: tag1, tag2, tag3\n"
        "[FUNCTION]: short_summary\n"
        "[CONNECTION_SCOPE]: global or local\n\n"
        "Content:\n"
        f"{content}\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

def write_tag_file(original_path, tag_content):
    """Write tag file next to original."""
    tag_path = Path(f"{original_path}.tag.txt")
    with open(tag_path, "w", encoding="utf-8") as f:
        f.write(tag_content)

def process_file(file_path):
    """Main logic: hash, check, tag, write."""
    try:
        file_hash = sha256_hash(file_path)
        if already_processed(file_hash):
            print(f"[=] Skipped (cached): {file_path}")
            return

        print(f"[+] Tagging: {file_path}")
        tag_data = generate_tags(file_path)
        write_tag_file(file_path, tag_data)
        append_to_cache(file_hash, file_path)

    except Exception as e:
        print(f"[!] Error processing {file_path}: {e}")

def scan_and_tag(directory):
    """Walk the directory and process supported files."""
    all_files = []
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            if Path(full_path).suffix.lower() in SUPPORTED_EXTENSIONS:
                all_files.append(full_path)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_file, all_files)

def main():
    parser = argparse.ArgumentParser(description="Semantic Logic Tagging Engine")
    parser.add_argument("directory", help="Root directory to scan for text files")
    args = parser.parse_args()

    print(f"[+] Scanning: {args.directory}")
    scan_and_tag(args.directory)
    print("[✓] Tagging complete.")

if __name__ == "__main__":
    main()
