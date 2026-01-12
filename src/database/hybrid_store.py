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
            # The Executive Ledger (Cold Storage)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS executive_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    cpu_percent REAL,
                    memory_percent REAL,
                    anomaly_score REAL,
                    prediction TEXT,
                    context_status TEXT,
                    action_taken TEXT
                )
            """)
            # The Antibody Database (L0)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS malware_signatures (
                    hash TEXT PRIMARY KEY,
                    threat_name TEXT,
                    source TEXT,
                    date_added DATETIME
                )
            """)
            conn.commit()

    # --- THE SCRIBE: This populates the DB ---
    def commit_event(self, event_data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO executive_ledger (
                        timestamp, cpu_percent, memory_percent, 
                        anomaly_score, prediction, context_status, action_taken
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    event_data.get('cpu_percent', 0.0),
                    event_data.get('memory_percent', 0.0),
                    event_data.get('anomaly_score', 0.0),
                    event_data.get('prediction', 'UNKNOWN'),
                    event_data.get('L3_contextual_status', 'NORMAL'),
                    event_data.get('L4_response_status', 'NONE')
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"[DB_ERROR] Failed to commit: {e}")

    # --- THE SCHOLAR: This reads for L5 Learning ---
    def get_learning_batch(self, limit=500):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT cpu_percent, memory_percent FROM executive_ledger 
                    WHERE context_status = 'NORMAL' 
                    ORDER BY timestamp DESC LIMIT ?
                """, (limit,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            return []

    # --- THE ANTIBODY METHODS ---
    def add_malware_hash(self, h, name, src):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO malware_signatures VALUES (?,?,?,?)", 
                         (h, name, src, datetime.now().isoformat()))

    def is_hash_malicious(self, h):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT 1 FROM malware_signatures WHERE hash=?", (h,)).fetchone() is not None

# The singleton instance used by all layers

store = HybridStore()