# src/database/hybrid_store.py

import sqlite3
import os
from datetime import datetime

class HybridStore:
    def __init__(self, db_path="logs/octopie_intelligence.db"):
        self.db_path = db_path
        self._ensure_directories()
        self._init_sqlite()

    def _ensure_directories(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # ... existing executive_ledger table ...
            
            # New: Malware Signature Table for Layer 0
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS malware_signatures (
                    hash TEXT PRIMARY KEY,
                    threat_name TEXT,
                    source TEXT,
                    date_added DATETIME
                )
            """)
            conn.commit()

    def add_malware_hash(self, file_hash, threat_name="Unknown", source="Manual"):
        """Inserts a new signature into the antibody database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO malware_signatures (hash, threat_name, source, date_added)
                    VALUES (?, ?, ?, ?)
                """, (file_hash, threat_name, source, datetime.now().isoformat()))
                conn.commit()
        except sqlite3.Error as e:
            print(f"[DB_ERROR] Failed to add hash: {e}")

    def is_hash_malicious(self, file_hash):
        """Checks if a hash exists in our known-bad ledger."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM malware_signatures WHERE hash = ?", (file_hash,))
            return cursor.fetchone() is not None

store = HybridStore()