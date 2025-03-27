import os

# Define USB Key Path (Adjust based on system)
USB_DRIVE_PATH = "E:/infinitykey.txt"

def get_usb_key():
    """Reads and validates USB key if present."""
    if os.path.exists(USB_DRIVE_PATH):
        with open(USB_DRIVE_PATH, "r") as key_file:
            secret_key = key_file.read().strip()

        if secret_key.startswith("SecretInfinityKey-"):
            return secret_key  # ✅ Valid Key
    return None  # ❌ No Key / Invalid Key
