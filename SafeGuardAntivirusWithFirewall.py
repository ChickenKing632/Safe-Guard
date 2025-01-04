import os
import hashlib
import logging
import mimetypes
import zipfile
import socket
import threading
from queue import Queue
from shutil import copy2

MALWARE_SIGNATURES = {
    'e99a18c428cb38d5f260853678922e03': {'name': 'Malware.Name.Here', 'source': 'Email Attachment'},
}

LOG_FILE = 'antivirus_log.txt'
QUARANTINE_DIRECTORY = 'quarantine'
BACKUP_DIRECTORY = 'backups'
THREAD_COUNT = 4  # Number of threads for scanning

class SimpleFirewall:
    def __init__(self, allowed_ports):
        self.allowed_ports = allowed_ports
        self.blocked_addresses = set()

    def block_address(self, address):
        self.blocked_addresses.add(address)

    def unblock_address(self, address):
        self.blocked_addresses.discard(address)

    def is_address_blocked(self, address):
        return address in self.blocked_addresses

    def is_port_allowed(self, port):
        return port in self.allowed_ports

def file_hash(filename, hash_algorithm='sha256', buffer_size=8192):
    hasher = hashlib.new(hash_algorithm)
    with open(filename, 'rb') as file:
        while (chunk := file.read(buffer_size)):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_file(filepath):
    try:
        if not os.path.isfile(filepath):
            logging.debug(f"Skipping non-file: {filepath}")
            return

        if not is_binary_file(filepath):
            logging.debug(f"Skipping non-binary file: {filepath}")
            return

        hash_value = file_hash(filepath)
        if hash_value in MALWARE_SIGNATURES:
            malware_info = MALWARE_SIGNATURES[hash_value]
            logging.warning(f"Malware detected: {malware_info['name']} in {filepath}")
            backup_and_move_to_quarantine(filepath)
        else:
            logging.info(f"No malware detected in {filepath}")
    except Exception as e:
        logging.error(f"Error scanning file {filepath}: {e}")

def is_binary_file(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime and 'text' not in mime

def backup_and_move_to_quarantine(file_path):
    os.makedirs(QUARANTINE_DIRECTORY, exist_ok=True)
    os.makedirs(BACKUP_DIRECTORY, exist_ok=True)
    copy2(file_path, os.path.join(BACKUP_DIRECTORY, os.path.basename(file_path)))
    os.rename(file_path, os.path.join(QUARANTINE_DIRECTORY, os.path.basename(file_path)))
    logging.info(f"File quarantined: {file_path}")

def worker(queue):
    while not queue.empty():
        filepath = queue.get()
        scan_file(filepath)
        queue.task_done()

def scan_directory(directory):
    file_queue = Queue()
    for root, _, files in os.walk(directory):
        for file in files:
            file_queue.put(os.path.join(root, file))

    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=worker, args=(file_queue,))
        thread.start()
        threads.append(thread)

    file_queue.join()
    for thread in threads:
        thread.join()

def configure_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_firewall(firewall, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    logging.info(f"Firewall listening on port {port}")

    while True:
        client_socket, address = server.accept()
        if not firewall.is_address_blocked(address[0]) and firewall.is_port_allowed(address[1]):
            logging.info(f"Accepted connection from {address}")
            client_socket.send(b"Connection allowed.")
        else:
            logging.warning(f"Blocked connection from {address}")
            client_socket.send(b"Connection blocked.")
            client_socket.close()

def main():
    configure_logging()

    allowed_ports = {80, 443, 8888}
    firewall = SimpleFirewall(allowed_ports)
    firewall_thread = threading.Thread(target=start_firewall, args=(firewall, 8888), daemon=True)
    firewall_thread.start()

    directory_to_scan = 'C:\\'  # Replace with the directory to scan
    try:
        logging.info("Starting directory scan...")
        scan_directory(directory_to_scan)
        logging.info("Directory scan completed.")
    except Exception as e:
        logging.error(f"Error during scanning: {e}")

if __name__ == "__main__":
    main()
