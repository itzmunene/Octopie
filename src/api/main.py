# src/api/main.py
from fastapi import FastAPI, HTTPException
from src.database.hybrid_store import store
import sqlite3

app = FastAPI(title="Octopie API - The Synapse")

# Helper to avoid repetitive connection logic
def get_db_connection():
    try:
        conn = sqlite3.connect(store.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database Unavailable")
    
    try:
        cursor = conn.cursor()
        # Ensure the table exists before querying to prevent errors
        cursor.execute("SELECT COUNT(*) FROM executive_ledger")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM malware_signatures")
        sigs = cursor.fetchone()[0]
        
        return {
            "total_events": total, 
            "signatures": sigs, 
            "status": "ACTIVE",
            "db_location": store.db_path
        }
    finally:
        conn.close()

@app.get("/ledger")
def get_ledger():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Fetching the last 100 events for the Dashboard
        cursor.execute("""
            SELECT id, timestamp, cpu_percent, memory_percent, 
                   anomaly_score, prediction, context_status, action_taken 
            FROM executive_ledger 
            ORDER BY timestamp DESC LIMIT 100
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

@app.get("/threats")
def get_threats():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM malware_signatures")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()