import os
import subprocess
from datetime import datetime
from zipfile import ZipFile

# === CONFIG ===
LOG_SOURCES = ["System", "Security", "Application"]  # Windows Event Logs
OUTPUT_DIR = "logs"

# === Ensure logs/ exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_event_log(log_name):
    """Export a Windows Event Log to an EVTX file using wevtutil."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{log_name}_{timestamp}.evtx"
    filepath = os.path.join(OUTPUT_DIR, filename)

    print(f"[+] Exporting log: {log_name}")
    try:
        subprocess.run(["wevtutil", "epl", log_name, filepath], check=True)
        print(f"[✓] Saved: {filepath}")
        return filepath
    except subprocess.CalledProcessError as e:
        if e.returncode == 5:
            print(f"[!] Access denied for log: {log_name}. Must have security clearance level 1 or higher(ADMIN PERMS).")
        else:
            print(f"[!] Failed to export {log_name}: {e}")
        return None

def zip_logs(filepaths):
    """Compress all collected log files into a single ZIP archive."""
    zip_name = os.path.join(OUTPUT_DIR, "logs_collected.zip")
    print(f"[+] Zipping logs into {zip_name}")
    with ZipFile(zip_name, 'w') as zipf:
        for f in filepaths:
            if f:
                zipf.write(f, arcname=os.path.basename(f))
    print("[✓] Compression complete.")
    return zip_name

def main():
    print("=== Secure Log Collector: Windows Mode ===")
    collected = [export_event_log(log) for log in LOG_SOURCES]
    zip_logs(collected)

if __name__ == "__main__":
    main()
