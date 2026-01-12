# src/layer0_integrity_monitor.py-catches known bad hash or a YARA rule.

import hashlib
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.database.hybrid_store import store

class IntegrityHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        print(f"[L0] New file detected: {file_path}")
        file_hash = self.get_file_hash(file_path)
        
        if store.is_hash_malicious(file_hash): # type: ignore
            print(f"\n[L0/ALERT] !!! MALICIOUS SIGNATURE DETECTED !!!")
            print(f"FILE: {file_path}")
            print(f"HASH: {file_hash}")
            self.quarantine(file_path)
        else:
            print(f"[L0] File Clean (Innate check).")

    def get_file_hash(self, file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"ERROR_{e}"

    def quarantine(self, file_path):
        print(f"[L0/RESPONSE] Quarantining {file_path}...")
        # Add logic to move file to a restricted folder or chmod 000
        pass

def run_integrity_scan(watch_path):
    print(f"--- [OCTOPIE] LAYER 0 INTEGRITY MONITOR ONLINE ---")
    print(f"Monitoring: {watch_path}")
    
    event_handler = IntegrityHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Test path - create a 'watch_folder' for testing
    path = "./watch_folder"
    if not os.path.exists(path): os.makedirs(path)
    run_integrity_scan(path)