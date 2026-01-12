# src/api/main.py
from fastapi import FastAPI
from src.database.hybrid_store import store
import sqlite3

app = FastAPI(title="Octopie API")

@app.get("/stats")
def get_stats():
    with sqlite3.connect(store.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM executive_ledger")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM malware_signatures")
        sigs = cursor.fetchone()[0]
        return {"total_events": total, "signatures": sigs, "status": "ACTIVE"}

@app.get("/ledger")
def get_ledger():
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM executive_ledger ORDER BY timestamp DESC LIMIT 100")
        return [dict(row) for row in cursor.fetchall()]

@app.get("/threats")
def get_threats():
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM malware_signatures")
        return [dict(row) for row in cursor.fetchall()]