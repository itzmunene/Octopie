# src/main.py
import asyncio
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.database.hybrid_store import store
from src.engine import run_autonomous_engine  # Our unified loop
import sqlite3

# --- 1. The Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Launch the Engine in a separate thread
    # We use a thread so the Engine doesn't block the API's event loop
    engine_thread = threading.Thread(target=run_autonomous_engine, daemon=True)
    engine_thread.start()
    print("🚀 [SYSTEM] Autonomous Engine launched in background thread.")
    
    yield
    
    # SHUTDOWN: Cleanup logic (if needed)
    print("🛑 [SYSTEM] Shutting down Octopie...")

app = FastAPI(title="Octopie Autonomous System", lifespan=lifespan)

# --- 2. Shared Database Helper ---
def get_db_connection():
    conn = sqlite3.connect(store.db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- 3. API Endpoints (The Synapse) ---

@app.get("/stats")
def get_stats():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM executive_ledger")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM malware_signatures")
        sigs = cursor.fetchone()[0]
        return {"total_events": total, "signatures": sigs, "status": "ACTIVE"}

@app.get("/ledger")
def get_ledger():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM executive_ledger ORDER BY timestamp DESC LIMIT 50")
        return [dict(row) for row in cursor.fetchall()]

@app.get("/health")
def health_check():
    return {"engine_status": "RUNNING", "database": store.db_path}