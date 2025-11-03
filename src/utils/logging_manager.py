"""
Simple logging wrapper - writes JSON lines to logs/telemetry.log
"""
import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_event(obj: dict, filename: str = "telemetry.log"):
    file_path = LOG_DIR / filename
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": datetime.utcnow().isoformat(), **obj}) + "\n")
