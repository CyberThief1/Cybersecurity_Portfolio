import os
import base64
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass

def derive_key_from_password(password: str) -> bytes:
    """Derive a Fernet-compatible key from a password using SHA256."""
    sha = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt_file(input_path, password):
    """Encrypt a file with Fernet and save it with .encrypted extension."""
    key = derive_key_from_password(password)
    fernet = Fernet(key)

    output_path = input_path + ".encrypted"

    with open(input_path, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(output_path, 'wb') as f:
        f.write(encrypted)

    print(f"[✓] Encrypted file saved as: {output_path}")

    # Optional: save hash of key for verification later
    with open(output_path + ".keyhash.txt", "w") as f:
        key_hash = hashlib.sha256(key).hexdigest()
        f.write(f"Password Hash: {key_hash}\n")
        f.write(f"Original File: {os.path.basename(input_path)}\n")
        print(f"[+] Password hash saved for verification.")

def main():
    print("=== Log File Encryptor ===")
    zip_path = input("Enter path to ZIP file to encrypt: ").strip()

    if not os.path.isfile(zip_path):
        print("[!] File does not exist.")
        return

    password = getpass("Enter encryption password: ")
    encrypt_file(zip_path, password)

if __name__ == "__main__":
    main()
