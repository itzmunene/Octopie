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
        
        if store.is_hash_malicious(file_hash):
            print(f"[L0/ALERT] MALICIOUS HASH: {file_hash}")
            self.quarantine(file_path)
        else:
            print(f"[L0] File Clean.")

    def get_file_hash(self, file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception:
            return "ERROR_READING_FILE"

    def quarantine(self, file_path):
        """Fixed: Defined os and destination logic"""
        os.makedirs("quarantine", exist_ok=True)
        filename = os.path.basename(file_path)
        dest = os.path.join("quarantine", filename)
        try:
            os.rename(file_path, dest)
            print(f"[L0/RESPONSE] Quarantined to {dest}")
            # Log to DB so Dashboard can show the alert
            store.commit_event({
                "cpu_percent": 0, "memory_percent": 0, "anomaly_score": 1.0,
                "prediction": "MALWARE", "context_status": "QUARANTINED",
                "action_taken": f"Isolated {filename}"
            })
        except Exception as e:
            print(f"[L0/ERROR] Quarantine failed: {e}")