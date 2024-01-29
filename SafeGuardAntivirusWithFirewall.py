import os
import hashlib
import logging
import mimetypes
import zipfile
import socket
import threading
import time
from shutil import copy2

# Known malware signatures with additional information
MALWARE_SIGNATURES = {
    'e99a18c428cb38d5f260853678922e03': {
        'name': 'Malware.Name.Here',
        'source': 'Email Attachment'
    },
    # Add more signatures here
}

# Log file, quarantine directory, and backup directory constants
LOG_FILE = 'antivirus_log.txt'
QUARANTINE_DIRECTORY = 'quarantine'
BACKUP_DIRECTORY = 'backups'

class SimpleFirewall:
    def __init__(self, allowed_ports):
        self.allowed_ports = allowed_ports
        self.blocked_addresses = set()

    def block_address(self, address):
        self.blocked_addresses.add(address)

    def unblock_address(self, address):
        if address in self.blocked_addresses:
            self.blocked_addresses.remove(address)

    def is_address_blocked(self, address):
        return address in self.blocked_addresses

    def is_port_allowed(self, port):
        return port in self.allowed_ports

def file_hash(filename, hash_algorithm='sha256', buffer_size=8192):
    """Calculate the hash of a file."""
    hasher = hashlib.new(hash_algorithm)
    with open(filename, 'rb') as file:
        buffer = file.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(buffer_size)
    return hasher.hexdigest()

def is_executable(file_path):
    """Check if a file is executable."""
    return os.access(file_path, os.X_OK)

def is_binary_file(file_path):
    """Check if a file is binary (not text)."""
    mime, _ = mimetypes.guess_type(file_path)
    return mime and 'text' not in mime

def scan_file(filepath, firewall):
    """Scan a single file for malware and provide user information."""
    try:
        if not is_executable(filepath):
            print(f"Skipping non-executable file: {filepath}")
            return

        if is_binary_file(filepath):
            print(f"Skipping binary file: {filepath}")
            return

        # Check if the file is an archive and scan its contents
        if zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, 'r') as archive:
                for file_info in archive.infolist():
                    file_data = archive.read(file_info.filename)
                    hash_value = hashlib.sha256(file_data).hexdigest()
                    scan_archive_file(file_info.filename, hash_value, firewall)
        else:
            hash_value = file_hash(filepath)
            scan_archive_file(filepath, hash_value, firewall)

    except Exception as e:
        print(f"Error scanning file {filepath}: {str(e)}")

def scan_archive_file(file_path, hash_value, firewall):
    """Scan an individual file within an archive."""
    malware_info = MALWARE_SIGNATURES.get(hash_value, None)

    if malware_info:
        malware_name = malware_info['name']
        malware_source = malware_info['source']
        print(f"Malware detected: {malware_name} in file {file_path} (from archive)")
        print(f"Source: {malware_source}")
        print("Recommendation: Delete the infected file or perform a more in-depth scan.")
        user_confirmation = input("Do you want to move the file to quarantine? (yes/no): ").lower()
        if user_confirmation == 'yes':
            backup_and_move_to_quarantine(file_path)
    else:
        print(f"No malware detected in file {file_path} (from archive)")

def backup_and_move_to_quarantine(file_path):
    """Create a backup of the file and move it to the quarantine directory."""
    backup_file(file_path)
    move_to_quarantine(file_path)

def backup_file(file_path):
    """Create a backup of the file in the backup directory."""
    if not os.path.exists(BACKUP_DIRECTORY):
        os.makedirs(BACKUP_DIRECTORY)

    backup_path = os.path.join(BACKUP_DIRECTORY, os.path.basename(file_path))
    copy2(file_path, backup_path)
    print(f"Backup created for {file_path} at {backup_path}")

def move_to_quarantine(file_path):
    """Move a file to the quarantine directory."""
    if not os.path.exists(QUARANTINE_DIRECTORY):
        os.makedirs(QUARANTINE_DIRECTORY)

    quarantine_path = os.path.join(QUARANTINE_DIRECTORY, os.path.basename(file_path))
    os.rename(file_path, quarantine_path)
    print(f"File moved to quarantine: {quarantine_path}")

def scan_directory(directory, firewall):
    """Scan a directory for files to be checked for malware."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            scan_file(filepath, firewall)

def configure_logging():
    """Configure secure logging."""
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def start_firewall(firewall, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Firewall listening on port {port}")

    while True:
        client_socket, address = server.accept()
        if not firewall.is_address_blocked(address[0]) and firewall.is_port_allowed(address[1]):
            print(f"Accepted connection from {address}")
            client_socket.send(b"Connection allowed.")
        else:
            print(f"Blocked connection from {address}")
            client_socket.send(b"Connection blocked.")
            client_socket.close()

def main():
    # Configure logging
    configure_logging()

    allowed_ports = {80, 443, 8888}  # You can customize the allowed ports
    firewall = SimpleFirewall(allowed_ports)

    firewall_thread = threading.Thread(target=start_firewall, args=(firewall, 8888))
    firewall_thread.daemon = True
    firewall_thread.start()

    # Specify the directory to scan
    directory_to_scan = 'C:\\'  # You can change this to any directory you wish to scan

    try:
        # Perform the scan
        scan_directory(directory_to_scan, firewall)

        # Log completion message
        logging.info(f'Completed scanning files in {directory_to_scan}.')
    except Exception as e:
        # Log errors
        logging.error(f'Error during scanning: {str(e)}')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting the firewall.")
        firewall_thread.join()

if __name__ == "__main__":
    main()
